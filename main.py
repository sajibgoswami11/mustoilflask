from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, Recipe, Tag, Ingredient, NutritionFact, Instruction, ShoppingItem
import uuid
from routes import register_routes
from seed import seed_database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'

CORS(app) #Enable CORS for all routes and origins
db.init_app(app)

# Helper function (example, adjust as needed)
def serialize_recipe(recipe):
    return {
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'category': recipe.category,
        'tags': [tag.name for tag in recipe.tags],
        'imageUrl': recipe.imageUrl,
        'prepTime': recipe.prepTime,
        'cookTime': recipe.cookTime,
        'servings': recipe.servings,
        'difficulty': recipe.difficulty,
        # Add other fields as necessary
    }

app.config['serialize_recipe'] = serialize_recipe  # Attach to app.config if needed

# Explicitly create tables within the application context
with app.app_context():
    db.create_all()
    seed_database(db)  # Seed immediately after creation

register_routes(app, db)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
