import json
from typing import Any, Optional

import redis

from src.config.setting import settings


class RedisClient:
    """Cliente para manejar operaciones de caché con Redis"""

    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            decode_responses=True,
        )

    def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor del caché.

        Args:
            key: Clave a buscar

        Returns:
            Valor deserializado o None si no existe
        """
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Error al obtener del caché: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Guarda un valor en el caché.

        Args:
            key: Clave
            value: Valor a guardar (será serializado a JSON)
            ttl: Tiempo de vida en segundos (por defecto usa CACHE_TTL)

        Returns:
            True si se guardó correctamente
        """
        try:
            ttl = ttl or settings.CACHE_TTL
            serialized = json.dumps(value)
            self.client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            print(f"Error al guardar en caché: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Elimina una clave del caché.

        Args:
            key: Clave a eliminar

        Returns:
            True si se eliminó
        """
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Error al eliminar del caché: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """
        Elimina todas las claves que coincidan con un patrón.

        Args:
            pattern: Patrón a buscar (ej: "events:*")

        Returns:
            Número de claves eliminadas
        """
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Error al eliminar patrón del caché: {e}")
            return 0

    def exists(self, key: str) -> bool:
        """
        Verifica si una clave existe en el caché.

        Args:
            key: Clave a verificar

        Returns:
            True si existe
        """
        return self.client.exists(key) > 0

    def ping(self) -> bool:
        """
        Verifica la conexión con Redis.

        Returns:
            True si la conexión es exitosa
        """
        try:
            return self.client.ping()
        except Exception:  # noqa: E722
            return False

    def clear_all(self) -> bool:
        """
        Limpia todas las claves del caché (solo para testing).

        ADVERTENCIA: ¡Esto elimina TODOS los datos en Redis!
        Solo usar en ambiente de testing.

        Returns:
            True si se limpió correctamente
        """
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            print(f"Error al limpiar caché: {e}")
            return False


# Instancia global del cliente
cache = RedisClient()
