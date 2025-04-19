from flask import jsonify, current_app, request
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

        # Update ingredients
        if 'ingredients' in data:
            existing_ingredients = {i.name: i for i in recipe.ingredients}
            updated_ingredients = data['ingredients']
            for ingredient_data in updated_ingredients:
                if ingredient_data['name'] in existing_ingredients:
                    # Update existing ingredient
                    ingredient = existing_ingredients.pop(ingredient_data['name'])
                    ingredient.quantity = ingredient_data['quantity']
                else:
                    # Add new ingredient
                    ingredient = Ingredient(
                        id=str(uuid.uuid4()),
                        name=ingredient_data['name'],
                        quantity=ingredient_data['quantity'],
                        recipe_id=id
                    )
                    db.session.add(ingredient)
            # Remove ingredients not in updated data
            for ingredient in existing_ingredients.values():
                db.session.delete(ingredient)

        # Update instructions
        if 'instructions' in data:
            existing_instructions = {i.stepNumber: i for i in recipe.instructions}
            updated_instructions = data['instructions']
            for instruction_data in updated_instructions:
                if instruction_data['stepNumber'] in existing_instructions:
                    # Update existing instruction
                    instruction = existing_instructions.pop(instruction_data['stepNumber'])
                    instruction.description = instruction_data['description']
                else:
                    # Add new instruction
                    instruction = Instruction(
                        id=str(uuid.uuid4()),
                        stepNumber=instruction_data['stepNumber'],
                        description=instruction_data['description'],
                        recipe_id=id
                    )
                    db.session.add(instruction)
            # Remove instructions not in updated data
            for instruction in existing_instructions.values():
                db.session.delete(instruction)

        # Update nutrition facts
        if 'nutrition_facts' in data:
            existing_nutrition = {nf.name: nf for nf in recipe.nutrition_facts}
            updated_nutrition = data['nutrition_facts']
            for nutrition_data in updated_nutrition:
                if nutrition_data['name'] in existing_nutrition:
                    # Update existing nutrition fact
                    nutrition = existing_nutrition.pop(nutrition_data['name'])
                    nutrition.quantity = nutrition_data['quantity']
                else:
                    # Add new nutrition fact
                    nutrition = NutritionFact(
                        id=str(uuid.uuid4()),
                        name=nutrition_data['name'],
                        quantity=nutrition_data['quantity'],
                        recipe_id=id
                    )
                    db.session.add(nutrition)
            # Remove nutrition facts not in updated data
            for nutrition in existing_nutrition.values():
                db.session.delete(nutrition)

        db.session.commit()

        updated_recipe = Recipe.query.get(id)  # Refresh recipe data
        db.session.commit()

        return jsonify({
            **updated_recipe.__dict__,
            'tags': [tag.name for tag in updated_recipe.tags],
            'ingredients': [{'name': i.name, 'quantity': i.quantity} for i in updated_recipe.ingredients],
            'instructions': [{'stepNumber': i.stepNumber, 'description': i.description} for i in updated_recipe.instructions],
            'nutrition_facts': [{'name': nf.name, 'quantity': nf.quantity} for nf in updated_recipe.nutrition_facts],
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