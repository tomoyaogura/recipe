# recipe
Plan for Recipe App

## Features:
1. Import Recipe
2. Browse Recipe
3. Create New Recipe
4. Select Recipe/ 献立
5. Export Shopping list/ what to buy to increase recipe
6. Select Current Ingredients

## DATA MODELS:
### Ingredients
1. Name
2. Type [Meat, Vegetables,　調味料]
3. Location sold [Ranch 99, Safeway, etc.]
4. On Shopping List
5. Low

###  Recipe:
1. Name
2. Picture
3. Ease [Time]
4. Ingredient [New line broken list of Ingredient Classes] OR [optional]
5. Directoins [List]
6. Notes

### Kondate:
1. Collection of recipes

## Workflow:
### Shopping:
1. Current shopping list + Top 5 items that maximize repertorie [Item X will unlock X recipes]
2. Export Shopping list to trello to a unique board
3. Shop organized by Location [Minimizes]
4. After shopping, tap on buttons to indicate stocked

### Help Decide:
1. List of recipes with given ingredients/ Sort by key words/ Time/ etc. Default filters exist [gochisou, etc.]
2. Column by 主菜　副菜
3. Randomizer
4. "I need to use xxx" -> get rid of ingredients

### Cooking: After selected recipe
1. Built-in timer
2. List by list instructions
3. Overview ingredients view
4. Multiple recipes in parallel?

### Adding new models:
1. Creating Ingredients -> Backend import from CSV
2. Creating new recipes -> Import script from cookpad with scrapy

### Option:
Video watching/ streaming

