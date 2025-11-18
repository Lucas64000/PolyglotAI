# PolyglotAI

**Application d'apprentissage de langues étrangères propulsée par l'IA**

Framework d'apprentissage de langues avec architecture multi-agents et multi-providers, conçu pour l'extensibilité et le type-safety

---

## 🎯 À Propos du Projet

PolyglotAI est une application de tutorat linguistique qui tire parti de l'intelligence artificielle pour offrir une expérience d'apprentissage conversationnelle et adaptative. Le projet démontre une architecture propre et extensible avec des design patterns avancés pour l'intégration de multiples fournisseurs LLM, avec Azure de déjà disponible.

### Objectif
Créer un tuteur de langues virtuel capable de :
- Converser naturellement dans la langue cible
- Corriger les erreurs avec bienveillance
- Adapter le contenu au niveau de l'utilisateur (A1 à C2)
- Générer des exercices personnalisés
- Suivre la progression de l'apprenant

---

## 📊 État du Projet

**Phase actuelle :** POC (Proof of Concept)  
**Branche :** `POC`

### ✅ Phase 1 : Infrastructure de Services (Terminé)
- ✅ Architecture multi-fournisseurs extensible (Azure OpenAI implémenté)
- ✅ Patterns Builder + Registry pour l'extensibilité
- ✅ Adaptateurs de messages pour compatibilité SDK
- ✅ Abstractions type-safe avec génériques Python
- ✅ Gestion de configuration (YAML + variables d'environnement)
- ✅ Singleton thread-safe pour la configuration

### 🚧 Phase 2 : POC Chatbot (En cours)
- [ ] Service de mémoire conversationnelle
- [ ] Agent tuteur de langue fonctionnel
- [ ] Interface Gradio pour démonstration
- [ ] Gestion basique de l'historique de conversation

### 📋 Phase 3 : MVP (Après POC)
- [ ] Tests unitaires et d'intégration
- [ ] Agent générateur d'exercices
- [ ] Agent correcteur détaillé
- [ ] Multi-utilisateurs avec profils
- [ ] Plusieurs langues cibles supportées
- [ ] Deuxième provider LLM (Mistral)
- [ ] Observabilité et logs structurés

---

### Design Patterns Utilisés
- **Builder Pattern** : Construction de configurations complexes de services LLM
- **Registry Pattern** : Enregistrement dynamique des fournisseurs de services (extensibilité)
- **Facade Pattern** : API simplifiée pour la création de services
- **Dependency Injection** : Couplage faible entre composants
- **Adapter Pattern** : Gestion de messages indépendante du SDK
- **Singleton Pattern** : Configuration centralisée thread-safe

### Structure du Projet
```
src/
├── agents/                # Agents IA (tuteur, exercices) - À venir
├── memory/                # Mémoire des agents - En cours 
├── services/              # Couche logique métier ✅
│   ├── builders/          # Builders de services avec registry ✅
│   ├── azure_service.py
│   └── service_facade.py  # Façade pour orchéstrer la création d'un ServiceLLM
├── clients/               # Wrappers de clients API ✅
│   ├── config/            # Configurations des clients ✅
│   └── azure_client.py
├── adapters/              # Adaptateurs de messages SDK ✅
│   └── llm_adapter/
├── models/                # Modèles métier ✅
│   ├── conversation_model.py
│   └── user_model.py
├── core/                  # Types et enums core ✅
│   ├── enums.py
│   └── exceptions/
└── utils/                 # Configuration et utilitaires ✅
    ├── config.py
    └── logger.py
app/                       # Interface Gradio - À venir
```

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Compte AzureAIFoundry 

### Installation

1. Cloner le dépôt
```bash
git clone https://github.com/Lucas64000/PolyglotAI.git
cd PolyglotAI
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. Configurer l'environnement
```bash
# Copier et éditer le fichier .env
cp .env.example .env
```

Ajouter vos identifiants API :
```env
AZURE_OPENAI_API_KEY=votre_clé
AZURE_OPENAI_ENDPOINT=votre_endpoint   (Vous devez déployer votre propre modèle)
```

4. Configurer les services dans `config.yaml`
```yaml
general:
  active_llm_service: azure

services:
  azure:
    model_name_default: gpt-4o
    api_version: 2025-01-01-preview
    extra:
      timeout: 60.0
      max_retries: 3
```

### Exemple d'Utilisation

```python
from src.services.service_facade import LLMFacade
from src.models.conversation_model import Message
from src.core.enums import Role
from src.utils.config import get_config

# Charger la configuration
config = get_config()

# Créer le service
service = LLMFacade.create_llm_service(
    service_name=config.active_llm_service,
    model_name="gpt-4o",
    temperature=0.7,
    max_tokens=1000
)

# Générer une réponse
message = Message(role=Role.USER, content="Bonjour!")
response = service.generate([message])
print(response.content)
```

---

## 🛠️ Points Techniques

### Type Safety
- Type hints complets avec génériques Python
- Classes abstraites pour les interfaces
- Paramètres de type indépendants du SDK

### Gestion de Configuration
- Séparation des secrets (`.env`) et paramètres (`config.yaml`)
- Configuration singleton thread-safe
- Paramètres par service avec valeurs par défaut

### Extensibilité
- Ajout de nouveaux providers via implémentation de builders
- Auto-enregistrement via décorateurs
- Aucune modification du code existant nécessaire 

### Gestion des Erreurs
- Hiérarchie d'exceptions personnalisées (`LLMError`, `LLMResponseError`, etc.)
- Retries automatiques gérés par le SDK 
- Configuration du timeout et max_retries via `config.yaml`

---

## 📦 Dépendances

Dépendances principales :
- `openai` - SDK Azure OpenAI
- `pyyaml` - Parsing de configuration
- `python-dotenv` - Gestion des variables d'environnement

---

## 🎯 Roadmap Détaillée

### 📅 Planning

#### ✅ Phase 1 : Infrastructure côté providers
**Statut :** ✅ Complété

- Architecture des services LLM
- Patterns et abstractions
- Configuration et gestion d'erreurs

#### 🚧 Phase 2 : Agents 
**Statut :** 🚧 En cours

**Livrables :**
- [ ] Mémoire conversationnelle 
- [ ] Agent tuteur de langue basique
- [ ] Interface Gradio simple (1 page de chat)
- [ ] Script de démonstration fonctionnel

**Critères de validation du POC :**
- ✅ Conversation fluide avec le tuteur IA
- ✅ Mémorisation du contexte conversationnel
- ✅ Interface web démontrable
- ✅ Architecture extensible prouvée

#### 📋 Phase 3 : MVP Production-Ready
**Statut :** 📋 Planifié

**Fondations MVP**
- [ ] Tests unitaires (couverture >70% du code critique)
- [ ] 2ème provider LLM (OpenAI)
- [ ] Logs structurés (JSON)
- [ ] Validation proactive de configuration

**Features Métier**
- [ ] Agent générateur d'exercices
- [ ] Agent correcteur avec feedback détaillé
- [ ] Système de niveaux CEFR (A1-C2)
- [ ] Support multi-langues (anglais, espagnol, allemand)

**Polish & Production**
- [ ] Interface Gradio améliorée (tabs, settings)
- [ ] Gestion multi-utilisateurs
- [ ] CI/CD avec GitHub Actions
- [ ] Documentation complète 

---

## 👤 Auteur

**Lucas64000**  
GitHub: [@Lucas64000](https://github.com/Lucas64000)