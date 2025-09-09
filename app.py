from fastapi import FastAPI, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from list_manager.grocery_list import GroceryList

app = FastAPI()
templates = Jinja2Templates(directory="./templates")

grocery_list = GroceryList()
recipe = None

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/edit", response_class=HTMLResponse)
async def edit(request: Request):
    return templates.TemplateResponse("edit.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def edit(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

class RecipeRequest(BaseModel):
    recipe_url: str = Field(min_length=1)

@app.post("/search-recipe")
def get_ingredients(recipe_url: RecipeRequest):
    global recipe
    recipe, code = grocery_list.search_link(recipe_url.recipe_url)
    if code == 200:
        return JSONResponse(content=recipe.to_json(), status_code=code)
    else:
        return JSONResponse(content={"ingredients": [], "yields": 0}, status_code=code)

@app.get("/grocery-list")
def get_grocery_list():
    items = grocery_list.get_items()
    return JSONResponse(content={"items": items}, status_code=
                        status.HTTP_200_OK if items else status.HTTP_404_NOT_FOUND)

class ScaleRequest(BaseModel):
    multiplier: float

@app.post("/scale-recipe")
def scale(request: ScaleRequest):
    recipe.scale(request.multiplier)
    return JSONResponse(content=recipe.to_json())

@app.get("/get-recipe")
def get_recipe():
    return JSONResponse(content=recipe.to_json())

@app.post("/add-recipe")
def add_recipe():
    global recipe
    grocery_list.add_all(recipe.get_items())
    recipe = None
    return JSONResponse(content={ "items": grocery_list.get_items()})

@app.post("/reset-grocery-list")
def reset_grocery_list():
    grocery_list.reset()
    return JSONResponse(content={"items": grocery_list.get_items()})

@app.get("/get-list-as-str")
def get_list_as_str():
    return JSONResponse(content={"list": str(grocery_list)})

class IngredientList(BaseModel):
    ingredients_list: str

@app.post("/add-ingredients")
def add_ingredients(request: IngredientList):
    ingredients_list = request.ingredients_list
    ingredients = ingredients_list.split("\n")
    grocery_list.add_all(ingredients)
    return JSONResponse(content={ "items": grocery_list.get_items()})