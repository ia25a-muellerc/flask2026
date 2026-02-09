import os

class Config:
    # Liest Variable aus .env (lokal) oder Render Settings (prod)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback_secret')
    DB_URL = os.environ.get('DATABASE_URL') 
    SESSION_COOKIE_NAME = 'simple_session'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 Stunden

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True