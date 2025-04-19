from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.String, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id', db.String, db.ForeignKey('tag.id'), primary_key=True)
)

class Recipe(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    imageUrl = db.Column(db.String)
    prepTime = db.Column(db.Integer)
    cookTime = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    difficulty = db.Column(db.String)

    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    nutrition_facts = db.relationship('NutritionFact', backref='recipe', lazy=True)
    instructions = db.relationship('Instruction', backref='recipe', lazy=True)
    tags = db.relationship('Tag', secondary=recipe_tags, backref=db.backref('recipes', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Ingredient(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.String, db.ForeignKey('recipe.id'))

class NutritionFact(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.String, db.ForeignKey('recipe.id'))

class Instruction(db.Model):
    id = db.Column(db.String, primary_key=True)
    stepNumber = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.String, db.ForeignKey('recipe.id'))

class ShoppingItem(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    unit = db.Column(db.String)
    isChecked = db.Column(db.Boolean, default=False)
