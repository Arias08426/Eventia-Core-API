"""
Pruebas de integración con Redis (caché)

Nota: Estas pruebas requieren que Redis esté corriendo.
Si Redis no está disponible, las pruebas se saltarán automáticamente.
"""
import pytest
from src.cache.redis_client import RedisClient


def is_redis_available():
    """Verifica si Redis está disponible"""
    try:
        client = RedisClient()
        return client.ping()
    except:
        return False


@pytest.mark.integration
class TestCacheIntegration:
    """Pruebas de integración con Redis"""
    
    @pytest.fixture
    def cache_client(self):
        """Fixture para cliente de caché"""
        client = RedisClient()
        # Limpiar caché antes de cada prueba
        try:
            client.clear_all()
        except:
            pass
        yield client
        # Limpiar después
        try:
            client.clear_all()
        except:
            pass
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis no está disponible")
    def test_cache_set_and_get(self, cache_client):
        """Prueba guardar y recuperar del caché"""
        # Arrange
        key = "test:key"
        value = {"name": "Test", "value": 123}
        
        # Act
        result_set = cache_client.set(key, value)
        result_get = cache_client.get(key)
        
        # Assert
        assert result_set is True
        assert result_get == value
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis no está disponible")
    def test_cache_get_nonexistent(self, cache_client):
        """Prueba obtener clave que no existe"""
        # Act
        result = cache_client.get("nonexistent:key")
        
        # Assert
        assert result is None
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis no está disponible")
    def test_cache_delete(self, cache_client):
        """Prueba eliminar del caché"""
        # Arrange
        key = "test:delete"
        cache_client.set(key, {"data": "test"})
        
        # Act
        result = cache_client.delete(key)
        value = cache_client.get(key)
        
        # Assert
        assert result is True
        assert value is None
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis no está disponible")
    def test_cache_delete_pattern(self, cache_client):
        """Prueba eliminar por patrón"""
        # Arrange
        cache_client.set("events:1", {"id": 1})
        cache_client.set("events:2", {"id": 2})
        cache_client.set("users:1", {"id": 1})
        
        # Act
        deleted_count = cache_client.delete_pattern("events:*")
        
        # Assert
        assert deleted_count == 2
        assert cache_client.get("events:1") is None
        assert cache_client.get("events:2") is None
        assert cache_client.get("users:1") is not None
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis no está disponible")
    def test_cache_exists(self, cache_client):
        """Prueba verificar existencia de clave"""
        # Arrange
        key = "test:exists"
        cache_client.set(key, {"data": "test"})
        
        # Act & Assert
        assert cache_client.exists(key) is True
        assert cache_client.exists("nonexistent") is False
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis no está disponible")
    def test_cache_ttl(self, cache_client):
        """Prueba que el TTL funcione (expiración)"""
        import time
        
        # Arrange
        key = "test:ttl"
        cache_client.set(key, {"data": "test"}, ttl=1)  # 1 segundo
        
        # Act - Verificar que existe inicialmente
        assert cache_client.get(key) is not None
        
        # Esperar 2 segundos
        time.sleep(2)
        
        # Assert - Debe haber expirado
        assert cache_client.get(key) is None
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis no está disponible")
    def test_cache_ping(self, cache_client):
        """Prueba verificar conexión con Redis"""
        # Act
        result = cache_client.ping()
        
        # Assert
        assert result is True