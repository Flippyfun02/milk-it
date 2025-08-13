from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from grocery_list import GroceryList

app = FastAPI()
grocery_list = GroceryList()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    html_path = Path("templates/index.html")
    html_content = html_path.read_text()
    return HTMLResponse(content=html_content)

class RecipeRequest(BaseModel):
    recipe_url: str

@app.post("/add-recipe")
def get_ingredients(recipe_url: RecipeRequest):
    # Here you’d plug in your existing Python scraper
    c = grocery_list.add_link(recipe_url.recipe_url)
    return {"items" : grocery_list.get_items(), "code" : c}