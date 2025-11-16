class ConversationalAgent(BaseAgent):
    """Agent par défaut qui discute avec l'utilisateur de n'importe quel topic sans demande spécifique"""
    def __init__(self, llm: ProviderLLM, memory: MemoryService):
        super().__init__(llm=llm, memory=memory)
        
    def run(self, message: Message, user: User) -> Any:
        system_prompt = self._build_prompt(user)
        historic_messages = self.memory.historic
        
        messages = [system_prompt]
        messages.extend(historic_messages)
        messages.append(message)
        
        try:
            response = self.llm.generate(messages)
            return response
        except Exception as e:
            logger.error(f"Une erreur est survenue pendant la génération de la réponse pour {user.name}: {e}")
            return "Veuillez réessayer."
    
    def _build_prompt(self, user: User) -> Message:
        return {"role": "system", "content": CONVERSATIONAL_PROMPT.format(user=user)}

class GrammarAgent(BaseAgent):
    """
    Cet agent permet de corriger les erreurs de grammaire faites par l'utilisateur. 
    Utilisé lorsque l'utilisateur demande explicitement des corrections, ou lors du recap de la conversation.
    """
    def __init__(self, llm: ProviderLLM):
        super().__init__(llm=llm)

        
    def run(self, message: Dict[str, str], user: User, conversation_history: List[Message]) -> Any:
        system_prompt = self._build_prompt(user)
        
        try:
            response = self.llm.generate([message], system_prompt, temperature=0.0)
            return response
        except Exception as e:
            logger.error(f"Une erreur est survenue pendant la génération de la réponse pour {user.name}: {e}")
            return "Veuillez réessayer."
    
    def _build_prompt(self, user: User) -> str:
        return GRAMMAR_PROMPT.format(user=user)
    

class MemoryAgent:
    """Gère l'accès et la mise à jour de la mémoire de l'utilisateur stocké dans un JSON (temporaire)."""

    PERSISTENCE_FILE = "src/services/db/memory_store.json"

    def __init__(self):
        self.memory_store = self._load_store()

    def _load_store(self) -> Dict[str, Any]:
        """Charge le store depuis le fichier JSON s'il existe."""
        if os.path.exists(self.PERSISTENCE_FILE):
            try:
                with open(self.PERSISTENCE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erreur lors du chargement de la mémoire ({e}). Initialisation à vide.")
                return {}
        return {}

    def save_store(self):
        """Sauvegarde le store actuel dans le fichier JSON."""
        with open(self.PERSISTENCE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.memory_store, f, indent=2, ensure_ascii=False)

    def _get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Récupère ou initialise les données de l'utilisateur."""
        if user_id not in self.memory_store:
            self.memory_store[user_id] = {
                "context_history": [],
                "learning_profile": {"target_language_errors": [], "goals": []}
            }
        return self.memory_store[user_id]

    def get_context_history(self, user_id: str, n: int = 5) -> List[Dict[str, str]]:
        """Retourne les N derniers échanges pour le contexte du LLM."""
        data = self._get_user_data(user_id)
        return data["context_history"][-n:]

    def update_history(self, user_id: str, role: str, content: str):
        """Ajoute un message à l'historique de la conversation."""
        data = self._get_user_data(user_id)
        data["context_history"].append({"role": role, "content": content})
        
        # On conserve uniquement les 10 derniers messages pour des raisons d'optimisation
        if len(data["context_history"]) > 10:
             data["context_history"].pop(0) 

    def register_error(self, user_id: str, original: str, correction: str, error_type: str):
        """Ajoute ou met à jour un type d'erreur dans le profil d'apprentissage."""
        data = self._get_user_data(user_id)
        
        found = False
        for error in data["learning_profile"]["target_language_errors"]:
            if error["original"] == original and error["correction"] == correction:
                error["count"] += 1
                error["last_seen"] = utc_now()
                found = True
                break
                
        if not found:
            data["learning_profile"]["target_language_errors"].append({
                "type": error_type,
                "original": original,
                "correction": correction,
                "count": 1,
                "last_seen": utc_now()
            })
            
    def get_top_errors(self, user_id: str, n: int = 3) -> List[Dict[str, Any]]:
        """Récupère les N erreurs les plus fréquentes de l'utilisateur."""
        data = self._get_user_data(user_id)
        errors = data["learning_profile"]["target_language_errors"]
        
        return sorted(errors, key=lambda x: x['count'], reverse=True)[:n]

    def get_conversation_context(self, user_id: str, n: int = 5) -> List[Dict[str, str]]:
        """Retourne l'historique formaté POUR le LLM (déjà au bon format)"""
        data = self._get_user_data(user_id)
        # Déjà au format {"role": "user", "content": "..."}
        return data["context_history"][-n:]
    
    def add_interaction(self, user_id: str, user_message: str, assistant_response: str):
        """Ajoute une interaction complète (user + assistant)"""
        self.update_history(user_id, "user", user_message)
        self.update_history(user_id, "assistant", assistant_response)
    
    def get_learning_context(self, user_id: str) -> str:
        """Retourne un résumé du profil d'apprentissage pour enrichir le prompt"""
        top_errors = self.get_top_errors(user_id, n=3)
        
        if not top_errors:
            return "Aucune erreur récurrente détectée pour l'instant."
        
        context = "Erreurs fréquentes de l'utilisateur :\n"
        for err in top_errors:
            context += f"- {err['type']}: '{err['original']}' → '{err['correction']}' (x{err['count']})\n"
        
        return context
    
class RouterAgent(BaseAgent):
    """Agent orchestrateur, appelle les différents agents en leur passant les outils nécessaires selon les requêtes de l'utilisateur"""
    def __init__(self, llm: ProviderLLM, memory: MemoryService, agents: Dict[str, BaseAgent]):
        super().__init__(llm, memory)
        self.agents = agents


    def run(self, message: Message, user: User) -> str:
        prompt = self._build_prompt(user)
        tool_calls = self.llm.generate_tool_calls(messages=[message], tools=self._get_schema_tools(user))
        
        if not tool_calls:
            logger.info("Le router n'a pas choisi de tools.")
            return "Veuillez réessayer"

        tool_responses: List[Any] = [] 

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            
            try:
                args_data = json.loads(tool_call.function.arguments)
                
                content = self._extract_content_for_agent(function_name, args_data)

                agent = self.agents.get(function_name)
                
                if agent and content is not None:
                    message_for_agent = {"role": "user", "content": content}
                    logger.info(f"Tool utilisé: {function_name} avec comme message: {content}")
                    
                    agent_result = agent.run(message_for_agent, user)
                    
                    tool_responses.append({
                        "agent": function_name,
                        "result": agent_result
                    })
                else:
                    logger.error(f"L'execution du tool {function_name} a échoué: Agent non trouvé ou contenu manquant.")
                    
            except json.JSONDecodeError as e:
                logger.error(f"Erreur lors du chargement des arguments au format JSON {function_name}: {e}")
            except Exception as e:
                logger.error(f"Erreur durant l'execution de l'agent pour la fonction {function_name}: {e}")

        return self._format_final_response(tool_responses)


    def _extract_content_for_agent(self, function_name: str, args_data: Dict[str, Any]) -> str | None:
        """Extrait le contenu du message pour l'agent cible."""
        
        if function_name == "call_grammar_agent":
            return args_data.get('text_to_analyze')
        elif function_name == "call_conversational_agent":
            return args_data.get('user_message')
        
        return None

    def _format_final_response(self, results: List[Dict[str, Any]]) -> str:
        """Fusionne les résultats de tous les agents pour l'utilisateur."""
        
        if not results:
            return "Aucun agent n'a pu répondre suite à l'exécution des outils."
            
        if len(results) == 1:
            return results[0]['result']
            
        final_text = "Voici ma réponse complète :\n\n"
        for item in results:
            agent_name = item['agent'].replace('call_', '').replace('_agent', '').capitalize()
            final_text += f"--- {agent_name} Response ---\n"
            final_text += item['result'] + "\n\n"
            
        return final_text.strip()

    def _build_prompt(self, user: User) -> Message:
        return {"role": "system", "content": ROUTER_PROMPT.format(user=user, tools=self._get_schema_tools(user))}

    def _get_schema_tools(self, user: User) -> List[ChatCompletionToolParam]:
        return [
            {
                "type": "function",  
                "function": {          
                    "name": "call_grammar_agent",
                    "description": (
                        "Utilise cet outil UNIQUEMENT pour les demandes explicites de correction grammaticale, conjugaison, ou vérification de syntaxe. "
                        "**La demande de correction DOIT prévaloir sur toute intention conversationnelle.** "
                        "Ne jamais l'utiliser pour répondre à une question ouverte."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text_to_analyze": {
                                "type": "string",
                                "description": (
                                "**EXTRAIS la ou les phrases à corriger.** Si l'utilisateur demande une correction, tu dois uniquement extraire le texte à corriger, pas la requête en elle même. Par exemple, si le message est 'I go cinema. Corrige si j'ai fait des fautes', tu extrais 'I go cinema'."
                                "Fais bien attention au contexte de la requête, l'utilisateur peut très bien demander de corriger en {user.native_language.value}, alors qu'il parle des fautes en {user.target_language.value}. "
                                "Dans ce là, tu dois porter ton attention sur le message {user.target_language.value} et pas sur le message {user.native_language.value}."
                                )
                            }
                        },
                    },
                    "required": ["text_to_analyze"],
                } ,
            },
            {
                "type": "function",
                "function": {
                    "name": "call_conversational_agent",
                    "description": (
                        "Utilise cet outil pour TOUTES les conversations générales, déclarations, salutations, questions ouvertes, ou comme agent par DÉFAUT lorsque l'intention n'est pas une demande explicite de correction."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_message": {
                                "type": "string",
                                "description": "Le message envoyé par l'utilisateur."
                            }
                        }, 
                        "required": ["user_message"],
                    }
                }
            }
        ]