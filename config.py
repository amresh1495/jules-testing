import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""
    # Production specific settings like database URI, etc.
    pass

# Dictionary to access configurations by name
config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig
)

# Optional: Function to get config based on environment variable
def get_config():
    env = os.getenv('FLASK_ENV', 'default')
    return config_by_name.get(env, DevelopmentConfig)
