from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from list_manager.grocery_list import GroceryList

app = FastAPI()
grocery_list = GroceryList()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    html_path = Path("templates/index.html")
    html_content = html_path.read_text()
    return HTMLResponse(content=html_content)

class RecipeRequest(BaseModel):
    recipe_url: str = Field(min_length=1)

@app.post("/add-recipe")
def get_ingredients(recipe_url: RecipeRequest):
    ingredients, code = grocery_list.add_link(recipe_url.recipe_url)
    print(code)
    return JSONResponse(content={"items": ingredients}, status_code=code)

@app.get("/grocery-list")
def get_grocery_list():
    items = grocery_list.get_items()
    return JSONResponse(content={"items": items}, status_code=
                        status.HTTP_200_OK if items else status.HTTP_404_NOT_FOUND)