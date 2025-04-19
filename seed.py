import uuid
from models import Recipe, Tag, Ingredient, NutritionFact, Instruction  # Import models directly

def seed_database(db):  # Pass db as an argument
    with db.session.begin():        
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
            print(f"Cleared table: {table.name}")  # Add this line



        recipes = [
            {
                'id': '1',
                'title': 'Thai Red Curry Fried Rice',
                'imageUrl': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
                'prepTime': 40,
                'servings': 2,                
                'category': 'Asian',
                'difficulty': 'medium',
                'tags': ['Thai', 'Curry', 'Rice'],
            },
            {
                'id': '2',
                'title': 'Mediterranean Chickpea Salad',
                'imageUrl': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
                'prepTime': 15,
                'servings': 4,                
                'category': 'Salads',
                'difficulty': 'easy',
                'tags': ['Vegetarian', 'Healthy', 'Mediterranean'],
            },
            {
                'id': '3',
                'title': 'Classic Beef Burger',
                'imageUrl': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
                'prepTime': 25,
                'servings': 4,                
                'category': 'American',
                'difficulty': 'medium',
                'tags': ['Beef', 'Burgers', 'Dinner'],
            },
            {
                'id': '4',
                'title': 'Vegetable Stir Fry',
                'imageUrl': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
                'prepTime': 20,
                'servings': 2,                
                'category': 'Asian',
                'difficulty': 'easy',
                'tags': ['Vegetarian', 'Quick', 'Healthy'],
            },
            {
                'id': '5',
                'title': 'Spaghetti Carbonara',
                'imageUrl': 'https://images.unsplash.com/photo-1546549032-9571cd6b27df?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
                'prepTime': 30,
                'servings': 4,                
                'category': 'Italian',
                'difficulty': 'medium',
                'tags': ['Pasta', 'Italian', 'Dinner'],
            },
            {
                'id': '6',
                'title': 'Avocado Toast with Eggs',
                'imageUrl': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
                'prepTime': 10,
                'servings': 1,                
                'category': 'Breakfast',
                'difficulty': 'easy',
                'tags': ['Breakfast', 'Quick', 'Healthy'],
            }
        ]

        detailedRecipe = {
            'id': 'seed-detailed-1',
            'title': 'Thai Red Curry Fried Rice - Detailed',
            'imageUrl': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
            'prepTime': 10,
            'cookTime': 30,
            'servings': 2,
            'category': 'Asian',
            'difficulty': 'medium',
            'tags': ['Thai', 'Curry', 'Rice'],
            'description': 'A flavorful Thai-inspired fried rice with red curry paste, vegetables, and your choice of protein. Perfect for a quick weeknight dinner.',
            'ingredients': [
                {'name': 'jasmine rice', 'quantity': '1 cup'},
                {'name': 'lean ground pork', 'quantity': '1.5 lb'},
                {'name': 'lime', 'quantity': '1'},
                {'name': 'shredded carrots', 'quantity': '1 (10 oz) bag'},
                {'name': 'sugar snap peas', 'quantity': '1 (8 oz) pkg'},
                {'name': 'Thai curry paste, red', 'quantity': '45 ml'},
                {'name': 'fish sauce', 'quantity': '2 tbsp'},
                {'name': 'salt', 'quantity': '1 tsp'},
            ],
            'instructions': [
                {
                    'stepNumber': 1,
                    'description': 'Cook rice according to package directions. Let cool slightly.'
                },
                {
                    'stepNumber': 2,
                    'description': 'Heat a large wok or skillet over high heat. Add ground pork and cook, breaking up meat, until no longer pink, about 5 minutes.'
                },
                {
                    'stepNumber': 3,
                    'description': 'Add curry paste and stir to coat the meat. Cook for 1 minute until fragrant.'
                },
                {
                    'stepNumber': 4,
                    'description': 'Add carrots and snap peas. Stir-fry until vegetables begin to soften, about 3 minutes.'
                },
                {
                    'stepNumber': 5,
                    'description': 'Add cooked rice, fish sauce, and lime juice. Stir-fry until everything is well combined and heated through, about 2 minutes.'
                },
                {
                    'stepNumber': 6,
                    'description': 'Season with salt to taste. Garnish with lime wedges and serve immediately.'
                }
            ],
            'nutritionFacts': {
                'calories': 450,
                'protein': 25,
                'carbs': 60,
                'fat': 12
            },
        }

        for recipe_data in recipes:
            recipe = Recipe(
                id="seed-" + recipe_data['id'],
                title=recipe_data['title'],
                imageUrl=recipe_data['imageUrl'],
                prepTime=recipe_data['prepTime'],
                servings=recipe_data['servings'],
                category=recipe_data['category'],
                difficulty=recipe_data['difficulty'],
            )
            for tag_name in recipe_data.get('tags', []):
                tag = db.session.query(Tag).filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(id=str(uuid.uuid4()), name=tag_name)
                    db.session.add(tag)
                recipe.tags.append(tag)
            db.session.add(recipe)

        detailed_recipe = Recipe(
            id=detailedRecipe['id'],
            title=detailedRecipe['title'],
            imageUrl=detailedRecipe['imageUrl'],
            prepTime=detailedRecipe['prepTime'],
            cookTime=detailedRecipe['cookTime'],
            servings=detailedRecipe['servings'],
            category=detailedRecipe['category'],
            difficulty=detailedRecipe['difficulty'],
            description=detailedRecipe.get('description', '')
        )
        for tag_name in detailedRecipe.get('tags', []):
            tag = db.session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(id=str(uuid.uuid4()), name=tag_name)
                db.session.add(tag)                
            detailed_recipe.tags.append(tag)

        for ingredient_data in detailedRecipe['ingredients']:
            ingredient = Ingredient(
                id=str(uuid.uuid4()),
                name=ingredient_data['name'],
                quantity=ingredient_data['quantity'],
                recipe=detailed_recipe
            )
            db.session.add(ingredient)

        nutrition = detailedRecipe.get('nutritionFacts', {})
        if nutrition:
            nutrition_fact = NutritionFact(
                id=str(uuid.uuid4()),
                name="Nutrition Facts",  # Or a more specific name if available
                quantity=f"{nutrition.get('calories', 0)} calories, {nutrition.get('protein', 0)}g protein, {nutrition.get('carbs', 0)}g carbs, {nutrition.get('fat', 0)}g fat",
                recipe=detailed_recipe
            )
            db.session.add(nutrition_fact)

        for instruction_data in detailedRecipe['instructions']:
            instruction = Instruction(
                id=str(uuid.uuid4()),
                stepNumber=instruction_data['stepNumber'],
                description=instruction_data['description'],
                recipe=detailed_recipe
            )
            db.session.add(instruction)

        db.session.add(detailed_recipe)
