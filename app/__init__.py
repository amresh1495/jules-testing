from flask import Flask

# Create Flask app instance
app = Flask(__name__)

# Import and register routes from app/routes.py
# We do this after creating 'app' to avoid circular imports
# and to ensure routes can be registered to the app instance.
from app.routes import register_routes
register_routes(app)

# Import models to ensure they are known, although not directly used here
from app import models
