from flask import jsonify, current_app
from models import db, Recipe, Tag, Ingredient, NutritionFact, Instruction, ShoppingItem
import uuid

def register_routes(app, db):
    @app.route('/api/recipes', methods=['GET'])
    def get_recipes():
        recipes = Recipe.query.all()
        return jsonify([{
            **recipe.__dict__,
            'tags': [tag.name for tag in recipe.tags],
            '_sa_instance_state': None  # Remove SQLAlchemy internal state for serialization
        } for recipe in recipes])

    @app.route('/api/recipes/<string:id>', methods=['GET'])
    def get_recipe(id):
        recipe = Recipe.query.get(id)
        if recipe:
            return jsonify({
                **recipe.__dict__,
                'tags': [tag.name for tag in recipe.tags],
                'ingredients': [{'name': i.name, 'quantity': i.quantity} for i in recipe.ingredients],
                'instructions': [{'stepNumber': i.stepNumber, 'description': i.description} for i in recipe.instructions],
                'nutrition_facts': [{'name': nf.name, 'quantity': nf.quantity} for nf in recipe.nutrition_facts],
                '_sa_instance_state': None
            })
        return jsonify({'message': 'Recipe not found'}), 404

    @app.route('/api/recipes', methods=['POST'])
    def create_recipe():
        data = request.get_json()
        if not data or not all(k in data for k in ('title', 'description', 'category', 'tags', 'imageUrl', 'prepTime', 'cookTime', 'servings', 'difficulty', 'ingredients', 'nutrition_facts', 'instructions')):
            return jsonify({'message': 'Invalid input'}), 400

        recipe_id = str(uuid.uuid4())
        new_recipe = Recipe(
            id=recipe_id,
            title=data['title'],
            description=data['description'],
            category=data['category'],
            imageUrl=data['imageUrl'],
            prepTime=data['prepTime'],
            cookTime=data['cookTime'],
            servings=data['servings'],
            difficulty=data['difficulty']
        )

        for tag_name in data.get('tags', []):
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(id=str(uuid.uuid4()), name=tag_name)
                db.session.add(tag)
            new_recipe.tags.append(tag)
        
        for ingredient_data in data.get('ingredients', []):
            ingredient = Ingredient(
                id=str(uuid.uuid4()),
                name=ingredient_data['name'],
                quantity=ingredient_data['quantity'],
                recipe_id=recipe_id
            )
            db.session.add(ingredient)

        for instruction_data in data.get('instructions', []):
            instruction = Instruction(
                id=str(uuid.uuid4()),
                stepNumber=instruction_data['stepNumber'],
                description=instruction_data['description'],
                recipe_id=recipe_id
            )
            db.session.add(instruction)

        for nutrition_data in data.get('nutrition_facts', []):
            nutrition = NutritionFact(
                id=str(uuid.uuid4()),
                name=nutrition_data['name'],
                quantity=nutrition_data['quantity'],
                recipe_id=recipe_id
            )
            db.session.add(nutrition)

        db.session.add(new_recipe)
        db.session.commit()

        return jsonify({
            **new_recipe.__dict__,
            'tags': [tag.name for tag in new_recipe.tags],
            'ingredients': [{'name': i.name, 'quantity': i.quantity} for i in new_recipe.ingredients],
            'instructions': [{'stepNumber': i.stepNumber, 'description': i.description} for i in new_recipe.instructions],
            'nutrition_facts': [{'name': nf.name, 'quantity': nf.quantity} for nf in new_recipe.nutrition_facts],
            '_sa_instance_state': None
        }), 201

    @app.route('/api/recipes/<string:id>', methods=['PUT'])
    def update_recipe(id):
        recipe = Recipe.query.get(id)
        if not recipe:
            return jsonify({'message': 'Recipe not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid input'}), 400

        recipe.title = data.get('title', recipe.title)
        recipe.description = data.get('description', recipe.description)
        recipe.category = data.get('category', recipe.category)
        recipe.imageUrl = data.get('imageUrl', recipe.imageUrl)
        recipe.prepTime = data.get('prepTime', recipe.prepTime)
        recipe.cookTime = data.get('cookTime', recipe.cookTime)
        recipe.servings = data.get('servings', recipe.servings)
        recipe.difficulty = data.get('difficulty', recipe.difficulty)

        # Update tags
        new_tags = data.get('tags', [])
        recipe.tags = []  # Clear existing tags
        for tag_name in new_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(id=str(uuid.uuid4()), name=tag_name)
                db.session.add(tag)
            recipe.tags.append(tag)

        # Update ingredients, instructions, and nutrition facts (basic update, can be improved)
        if 'ingredients' in data:
            recipe.ingredients = []
            for ingredient_data in data['ingredients']:
                ingredient = Ingredient(
                    id=str(uuid.uuid4()),
                    name=ingredient_data['name'],
                    quantity=ingredient_data['quantity'],
                    recipe_id=id
                )
                db.session.add(ingredient)
                recipe.ingredients.append(ingredient)

        if 'instructions' in data:
            recipe.instructions = []
            for instruction_data in data['instructions']:
                instruction = Instruction(
                    id=str(uuid.uuid4()),
                    stepNumber=instruction_data['stepNumber'],
                    description=instruction_data['description'],
                    recipe_id=id
                )
                db.session.add(instruction)
                recipe.instructions.append(instruction)

        if 'nutrition_facts' in data:
            recipe.nutrition_facts = []
            for nutrition_data in data['nutrition_facts']:
                nutrition = NutritionFact(
                    id=str(uuid.uuid4()),
                    name=nutrition_data['name'],
                    quantity=nutrition_data['quantity'],
                    recipe_id=id
                )
                db.session.add(nutrition)
                recipe.nutrition_facts.append(nutrition)


        db.session.commit()

        return jsonify({
            **recipe.__dict__,
            'tags': [tag.name for tag in recipe.tags],
            'ingredients': [{'name': i.name, 'quantity': i.quantity} for i in recipe.ingredients],
            'instructions': [{'stepNumber': i.stepNumber, 'description': i.description} for i in recipe.instructions],
            'nutrition_facts': [{'name': nf.name, 'quantity': nf.quantity} for nf in recipe.nutrition_facts],
            '_sa_instance_state': None
        })

    @app.route('/api/recipes/<string:id>', methods=['DELETE'])
    def delete_recipe(id):
        recipe = Recipe.query.get(id)
        if not recipe:
            return jsonify({'message': 'Recipe not found'}), 404

        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted'})