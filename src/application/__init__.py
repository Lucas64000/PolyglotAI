"""
Application Layer

This layer contains:
- Use Cases: Single-purpose application operations
- Services: Orchestration of use cases and domain logic
- DTOs: Data Transfer Objects for API communication
- Agents: LLM-based agents for intelligent tutoring

RULES:
- Depends only on Core layer (domain entities, ports)
- NO direct infrastructure dependencies (databases, APIs)
- Receives infrastructure via dependency injection
"""
