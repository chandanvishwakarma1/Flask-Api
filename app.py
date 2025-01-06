from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data
recipes = [
    {"id": 1, "name": "Spaghetti Bolognese", "ingredients": ["spaghetti", "meat", "tomato sauce"], "instructions": "Cook the pasta, then add the sauce."},
    {"id": 2, "name": "Chicken Curry", "ingredients": ["chicken", "curry powder", "coconut milk"], "instructions": "Cook the chicken, then add the curry powder and coconut milk."},
]

# Home route to render all recipes and handle CRUD actions
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            # Add a new recipe
            name = request.form.get('name')
            ingredients = request.form.get('ingredients').split(',')  # Comma-separated input
            instructions = request.form.get('instructions')
            if name and ingredients and instructions:
                new_id = max(recipe['id'] for recipe in recipes) + 1 if recipes else 1
                recipes.append({"id": new_id, "name": name, "ingredients": ingredients, "instructions": instructions})
        return redirect(url_for('home'))
    return render_template('index.html', recipes=recipes)

# View individual recipe details
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if recipe:
        return render_template('recipes.html', recipe=recipe)
    return redirect(url_for('home'))

# Edit route (post data)
@app.route('/edit', methods=['POST'])
def edit_recipe():
    recipe_id = int(request.form.get('recipe_id'))
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if recipe:
        recipe['name'] = request.form.get('name', recipe['name'])
        recipe['ingredients'] = request.form.get('ingredients', ','.join(recipe['ingredients'])).split(',')
        recipe['instructions'] = request.form.get('instructions', recipe['instructions'])
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

# Delete route
@app.route('/delete', methods=['POST'])
def delete_recipe():
    recipe_id = int(request.form.get('recipe_id'))
    global recipes
    recipes = [r for r in recipes if r['id'] != recipe_id]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
