"""
Neo4j Connection Manager

Handles Neo4j driver lifecycle and connection pooling.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from neo4j import AsyncDriver

if TYPE_CHECKING:
    from types import TracebackType


class Neo4jConnection:
    """
    Manages Neo4j connection lifecycle.
    
    Provides:
    - Async driver management
    - Connection pooling
    - Health checks
    """
    
    def __init__(
        self,
        uri: str,
        user: str,
        password: str,
    ) -> None:
        """
        Initialize connection manager.
        
        Args:
            uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
            user: Neo4j username
            password: Neo4j password
        """
        self._uri = uri
        self._user = user
        self._password = password
        self._driver: AsyncDriver | None = None
    
    async def connect(self) -> AsyncDriver:
        """
        Create and return the Neo4j async driver.
        
        Returns:
            Configured AsyncDriver instance
        """
        if self._driver is None:
            from neo4j import AsyncGraphDatabase
            
            self._driver = AsyncGraphDatabase.driver(  # type: ignore[misc]
                self._uri,
                auth=(self._user, self._password),
            )
        return self._driver
    
    async def close(self) -> None:
        """Close the driver connection."""
        if self._driver is not None:
            await self._driver.close()
            self._driver = None
    
    async def verify_connectivity(self) -> bool:
        """
        Verify that the database is reachable.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            driver = await self.connect()
            await driver.verify_connectivity()  # type: ignore[misc]
            return True
        except Exception:
            return False
    
    @property
    def driver(self) -> AsyncDriver | None:
        """Get the current driver instance (may be None)."""
        return self._driver
    
    async def __aenter__(self) -> Neo4jConnection:
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        await self.close()
