# PolyglotAI

**Application d'apprentissage de langues étrangères propulsée par l'IA**

Framework d'apprentissage de langues avec architecture multi-providers extensible, système de mémoire conversationnelle et gestion avancée du contexte.

---

## 🎯 À Propos du Projet

PolyglotAI est une application de tutorat linguistique qui tire parti de l'intelligence artificielle pour offrir une expérience d'apprentissage conversationnelle et adaptative. Le projet démontre une architecture propre et extensible avec des design patterns avancés pour l'intégration de multiples fournisseurs LLM, avec Azure de déjà disponible.

### Objectif
Créer un tuteur de langues virtuel capable de :
- Converser naturellement dans la langue cible
- Corriger les erreurs avec bienveillance
- Maintenir le contexte conversationnel à long terme
- Adapter le contenu au niveau de l'utilisateur (A1 à C2)
- Générer des exercices personnalisés
- Suivre la progression de l'apprenant

---

## 📊 État du Projet

**Phase actuelle :** POC (Proof of Concept)  
**Branche :** `POC`

### ✅ Phase 1 : Infrastructure LLM (Terminé)
- ✅ Architecture multi-providers extensible (Azure OpenAI implémenté)
- ✅ Patterns Builder + Registry pour l'extensibilité
- ✅ Adaptateurs de messages type-safe pour compatibilité SDK
- ✅ Abstractions génériques Python avec type hints complets
- ✅ Gestion de configuration (YAML + variables d'environnement)
- ✅ Factory pattern pour création de providers LLM

### 🚧 Phase 2 : POC Chatbot (En cours)
- [ ] Service de mémoire conversationnelle
- [ ] Agent tuteur de langue fonctionnel
- [ ] Interface Gradio pour démonstration
- [ ] Gestion basique de l'historique de conversation

### 📋 Phase 3 : MVP (Après POC)
- [ ] Tests unitaires et d'intégration
- [ ] Agent générateur d'exercices
- [ ] Multi-utilisateurs avec profils
- [ ] Plusieurs langues cibles supportées
- [ ] Deuxième provider LLM (OpenAI API)
- [ ] Monitoring et observabilité

---

## 🏗️ Architecture & Design Patterns

### Design Patterns Implémentés
- **Factory Pattern** : Création centralisée de providers LLM (`LLMFactory`)
- **Builder Pattern** : Construction de configurations complexes de services
- **Registry Pattern** : Enregistrement dynamique des builders (extensibilité)
- **Repository Pattern** : Abstraction de la persistance des conversations
- **Strategy Pattern** : Stratégies de récupération mémoire interchangeables
- **Adapter Pattern** : Conversion des messages entre formats métier et SDK
- **Adapter Pattern** : Gestion de messages indépendante du SDK
- **Singleton Pattern** : Configuration centralisée thread-safe

### Structure du Projet
```
src/
├── services/              
│   ├── llm/               # Services LLM ✅
│   │   ├── providers/     # Providers (Azure) ✅
│   │   ├── builders/      # Builders avec registry ✅
│   │   ├── adapters/      # Adaptateurs de messages ✅
│   │   └── llm_factory.py # Factory de création ✅
│   └── memory/            # Système de mémoire ✅
│       ├── repositories/  # Persistence (JSON pour l'instant) ✅
│       └── strategies/    # Stratégies de récupération ✅
├── clients/               # Wrappers de clients API ✅
│   ├── config/            # Configurations des clients ✅
│   └── azure_client.py
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
- Compte Azure AI Foundry avec un modèle déployé

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

Ajouter vos identifiants Azure :
```env
AZURE_OPENAI_API_KEY=votre_clé
AZURE_OPENAI_ENDPOINT=votre_endpoint
```

4. Configurer les services dans `config.yaml`
```yaml
general:
  default_provider: azure

services:
  providers:
    azure:
      model_name_default: gpt-4o
      api_version: 2025-01-01-preview
      extra:
        timeout: 60.0
        max_retries: 3
```

### Lancer l'Application

```bash
python chatbot.py
```

### Exemple d'Utilisation du Code

```python
from src.services.llm.llm_factory import LLMFactory
from src.services.memory.repositories.json_repository import JsonFileMemoryRepository
from src.services.memory.strategies.window_strategy import WindowMemoryStrategy
from src.models.conversation_model import Message
from src.core.enums import Role
from uuid import uuid4

# Créer le provider LLM
llm = LLMFactory.create_llm_provider(
    provider_name="azure",
    model_name="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000
)

# Initialiser le système de mémoire
memory_repo = JsonFileMemoryRepository(storage_dir="data/conversations")
memory_strategy = WindowMemoryStrategy(repository=memory_repo, window_size=10)

# Créer une conversation
conversation_id = uuid4()

# Ajouter un message utilisateur
user_message = Message(
    conversation_id=conversation_id,
    role=Role.USER,
    content="Bonjour ! Comment allez-vous ?"
)
memory_strategy.add_message(user_message)

# Récupérer l'historique et générer une réponse
history = memory_strategy.get_context(conversation_id)
response = llm.generate(history, conversation_id)

# Sauvegarder la réponse
memory_strategy.add_message(response)

print(f"Assistant: {response.content}")
```

---

## 🛠️ Points Techniques

### Type Safety & Génériques
- Type hints complets avec génériques Python (`TypeVar`)
- Classes abstraites pour toutes les interfaces
- Paramètres de type indépendants du SDK (`TMessage`, `TResponse`)
- Validation Pydantic pour les modèles métier

### Gestion de Configuration
- Séparation des secrets (`.env`) et paramètres (`config.yaml`)
- Configuration singleton thread-safe avec lazy loading
- Paramètres par provider avec valeurs par défaut
- Validation proactive au démarrage

### Architecture Extensible
- Ajout de nouveaux providers via Builder pattern
- Auto-enregistrement via Registry pattern
- Aucune modification du code existant nécessaire
- Stratégies de mémoire interchangeables (Strategy pattern)

### Système de Mémoire
- **Persistence JSON** : Un fichier par conversation pour isolation
- **Thread-safe** : Opérations concurrentes avec `threading.RLock`
- **Window Strategy** : Récupération efficace des N derniers messages
- **Update avec troncature** : Modification de messages avec suppression de la suite
- **Atomic writes** : Écriture via fichier temporaire + renommage

### Gestion des Erreurs
- Hiérarchie d'exceptions personnalisées (`LLMError`, `LLMResponseError`, etc.)
- Retries automatiques gérés par le SDK 
- Configuration du timeout et max_retries via `config.yaml`
- Rollback automatique en cas d'erreur de sauvegarde mémoire

## 📦 Dépendances

### Dépendances principales
- `openai` (>=1.0.0) - SDK OpenAI
- `pyyaml` - Parsing de configuration YAML
- `python-dotenv` - Gestion des variables d'environnement
- `pydantic` - Validation des modèles de données

### Structure de données
- Conversations stockées en JSON (format lisible)
- Un fichier par conversation (`<conversation_id>.json`)
- Répertoire par défaut : `data/conversations/`

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
- ✅ Mémoire conversationnelle 
- [ ] Agent tuteur de langue basique
- [ ] Interface Gradio simple (1 page de chat)
- ✅ Script de démonstration fonctionnel


#### 📋 Phase 3 : MVP Production-Ready
**Statut :** 📋 Planifié

**Fondations MVP**
- [ ] Tests unitaires (couverture >70% du code critique)
- [ ] Logs structurés (JSON)
- [ ] Validation proactive de configuration

**Features Métier**
- [ ] Agent générateur d'exercices
- [ ] Agent correcteur avec feedback détaillé
- [ ] Système de niveaux CECRL (A1-C2)

**Polish & Production**
- [ ] Interface Gradio 
- [ ] Gestion multi-utilisateurs
- [ ] CI/CD avec GitHub Actions

---

## 👤 Auteur

**Lucas64000**  
GitHub: [@Lucas64000](https://github.com/Lucas64000)