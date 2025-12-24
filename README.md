# PolyglotAI

> A linguistic tutoring AI designed with strict Hexagonal Architecture.

![Status](https://img.shields.io/badge/Status-Development-yellow)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Architecture](https://img.shields.io/badge/Architecture-Hexagonal-orange)

## Technical Objective

This project serves as a technical demonstrator for a Python application designed for **Production-Ready** standards. The focus is on:

- **Framework Independence**: The business core (`Core`) has no dependencies (no DB, no Web, no LLM)
- **Testability**: The architecture enables testing business logic without mocking everything
- **Quality**: Strict typing, SOLID principles, comprehensive documentation, and TDD
- **Clean Code**: Professional-grade docstrings, type hints, and consistent naming conventions

## Architecture

The project strictly follows the **Ports & Adapters** (Hexagonal Architecture) pattern:

```
├── src
│   ├── core                    # Domain Layer (Pure Python, zero dependencies)
│   │   ├── domain              # Entities, Value Objects
│   │   │   ├── entities        
│   │   │   └── value_objects   
│   │   ├── ports               # Driven Interfaces (Abstractions)
│   │   └── exceptions          # Domain errors & invariant violations
│   │
│   ├── application             # Application Layer (Use Cases & Orchestration)
│   │   ├── commands            # Write operations (CQRS)         
│   │   ├── queries             # Read operations (CQRS)   
│   │   ├── dtos                # Commands (input) & Read Models (output) - Anti-corruption layer      
│   │   └── ports               # Application-specific driven interfaces (mainly readers)
│   │       
│   │
│   └── infrastructure          # Adapters (API / CLI, Repositories, AI Services)
│       ├── adapters
│       │   ├── driven          # Concrete implementation of Driven Interfaces 
│       │   └── driving         # Concrete implementation of Driving Interfaces    
│       ├── exceptions          # Infrastructure exceptions (API, HTTP, DB Erros etc.)      
│       └── container.py        # Dependency Injection configuration
│
└── tests                       # Unit tests (mirrors src/ structure)
    ├── conftest.py             # Shared pytest fixtures
    ├── core                    # Domain tests
    │   └── domain
    ├── application             # Use case tests
    ├── infrastructure          # Infrastructure tests
    └── doubles                 # Test doubles (fakes, stubs, mocks)
        ├── fakes               # Fake implementations (in-memory repositories, etc.)
        └── stubs               # Stub implementations (time providers, etc.)
```

## Design Principles

### Hexagonal Architecture (Ports & Adapters)

- **Core Domain**: Business logic with zero infrastructure dependencies
- **Application Layer**: Use cases orchestrating domain operations
- **Infrastructure**: Concrete implementations of ports (databases, APIs, AI services)
- **Dependency Inversion**: Dependencies point inward (infrastructure depends on core, not vice versa)

### CQRS (Command Query Responsibility Segregation)

- **Commands**: Write operations that modify state 
- **Queries**: Read operations that return data
- **Read Models**: Optimized data structures for queries

## Rich Domain Model

### Entities (Identity-Based)

- **User**: Learner with native/target language and proficiency level
- **Conversation**: Dialogue thread between user and AI tutor
- **ChatMessage**: Individual message in a conversation
- **VocabularyItem**: Tracked word with review history

### Value Objects (Value-Based)

- **Language**: ISO 639-1 language code
- **CEFRLevel**: Common European Framework levels (A1-C2)
- **Role**: Message sender role (SYSTEM, USER, ASSISTANT)
- **Status**: Conversation status (ACTIVE, ARCHIVED, DELETED)
- **TutorProfile**: AI configuration (creativity level, generation style)
- **Linguistics**: PartOfSpeech, Gender, Tense, Morphology, Lemma, Lexeme, etc.

## Stack

**Note**: The stack is still under development and may be modified.

- **Language**: Python 3.12+
- **Web Framework**: FastAPI (HTTP API layer)
- **Validation**: Pydantic (API DTOs)
- **Typing**: Strict type hints throughout
- **Dependency Injection**: API's dependency injection system
- **AI**: OpenAI / Azure / Ollama (interchangeable via Strategy pattern) (planned)
- **Persistence**: Neo4j (planned) / In-Memory (current development implementation)
- **Testing**: pytest 

## Getting Started

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/Lucas64000/PolyglotAI.git
cd PolyglotAI

# Install dependencies (development mode)
pip install -e .

# For development dependencies
pip install -e ".[dev]"

# Run the application
python -m uvicorn src.infrastructure.adapters.driving.fastapi.main:app --reload # There will be a run script later 
```

### API Documentation

Once the application is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/core/domain/entities/test_user.py
```

## Code Quality

- **Type Safety**: Strict typing with mypy compatibility
- **Immutability**: Extensive use of frozen dataclasses
- **Encapsulation**: Private attributes with property accessors
- **Validation**: Business rules enforced at domain level
- **Error Handling**: Domain-specific exceptions with clear messages

## Contributing

This project follows strict coding standards:

1. **All code must have comprehensive docstrings**
2. **Type hints are mandatory**
3. **Business logic belongs in the core domain**
4. **Infrastructure must be pluggable via ports**
5. **Tests must not depend on implementation details**

## License

See [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Clean Architecture (Robert C. Martin)
- Hexagonal Architecture (Alistair Cockburn)
- Domain-Driven Design (Eric Evans)
- CQRS pattern (Greg Young)
