import os

class Config:
    # Liest Variable aus .env (lokal) oder Render Settings (prod)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback_secret')
    DB_URL = os.environ.get('DATABASE_URL') 
    SESSION_COOKIE_NAME = 'simple_session'
    # Session ist nur während Browser-Sitzung gültig (nicht persistent)
    SESSION_COOKIE_HTTPONLY = True  # Schutz vor XSS
    SESSION_COOKIE_SAMESITE = 'Lax'  # Schutz vor CSRF
    SESSION_COOKIE_SECURE = False  # True auf Production mit HTTPS

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # HTTPS only auf Production
