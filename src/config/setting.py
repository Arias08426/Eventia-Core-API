"""
Configuración centralizada de la aplicación usando Pydantic Settings.

Lee las variables de entorno del archivo .env o del sistema.
"""
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Todas las variables se pueden definir en:
    1. Archivo .env en la raíz del proyecto
    2. Variables de entorno del sistema
    3. Valores por defecto definidos aquí

    Prioridad: Variables de entorno > .env > valores por defecto
    """

    # ============================================
    # INFORMACIÓN DE LA APLICACIÓN
    # ============================================
    APP_NAME: str = "Eventia Core API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # ============================================
    # CONFIGURACIÓN DEL SERVIDOR
    # ============================================
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ============================================
    # CONFIGURACIÓN DE BASE DE DATOS
    # ============================================
    DATABASE_URL: str = "mysql+pymysql://eventia:eventia@localhost:3306/eventia_test"
    """
    URL de conexión a MySQL.

    Formato: mysql+pymysql://usuario:contraseña@host:puerto/nombre_db
    Ejemplo: mysql+pymysql://eventia_user:eventia_pass@localhost:3306/eventia_db
    """

    DB_ECHO: bool = False
    """
    Si es True, SQLAlchemy imprime todas las queries SQL.
    Útil para debugging, desactivar en producción.
    """

    # ============================================
    # CONFIGURACIÓN DE REDIS (CACHÉ)
    # ============================================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    CACHE_TTL: int = 300
    """
    Time To Live del caché en segundos.
    Por defecto: 300 segundos (5 minutos)
    """

    # ============================================
    # CONFIGURACIÓN DE CORS
    # ============================================
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    """
    Lista de orígenes permitidos para CORS.
    Agregar aquí las URLs de tu frontend.
    """

    # ============================================
    # CONFIGURACIÓN DE LOGGING
    # ============================================
    LOG_LEVEL: str = "INFO"
    """
    Nivel de logging.
    Opciones: DEBUG, INFO, WARNING, ERROR, CRITICAL
    """

    class Config:
        """Configuración de Pydantic Settings"""

        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Permitir variables extras en .env sin fallar
        """
        case_sensitive = True significa que DATABASE_URL y database_url
        son diferentes variables.

        extra = "ignore" permite que haya variables en .env que no estén
        definidas en la clase Settings sin causar errores.
        """


# ============================================
# INSTANCIA GLOBAL DE CONFIGURACIÓN
# ============================================
settings = Settings()
"""
Instancia global de configuración.

Uso:
    from src.config.settings import settings

    print(settings.APP_NAME)
    print(settings.DATABASE_URL)
"""
