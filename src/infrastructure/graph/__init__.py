"""
Graph Infrastructure Module

Contains:
- Ontology definitions (nodes and edges for Neo4j)
- Graphiti adapter (implements GraphMemory port)
- Neo4j connection management
- Domain entity <-> Graph node mappers
"""

from .graphiti_adapter import GraphitiAdapter
from .neo4j_connection import Neo4jConnection

__all__ = [
    "GraphitiAdapter",
    "Neo4jConnection",
]
