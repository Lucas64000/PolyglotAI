"""
Application Layer Package

This package implements the Application Layer.
It contains the application logic that orchestrates domain objects and external services.

Contents:
- commands/: Command-side operations (write operations)
  - use_cases/: Application services for commands
  - dtos/: Data Transfer Objects for command requests/responses
- queries/: Query-side operations (read operations)
  - read_models/: Lightweight read models for efficient queries
  - use_cases/: Query application services
- ports/: Application ports defining interfaces for external dependencies

Architecture Rules:
- Depends only on the Core layer (domain entities and ports)
- No direct dependencies on infrastructure (databases, external APIs, frameworks)
- Receives infrastructure implementations via dependency injection
- Follows CQRS pattern with separate command and query sides
- Uses DTOs for external communication
- Uses Read Models for internal communication
"""
