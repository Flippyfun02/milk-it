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
    url: str

@app.post("/convert")
def convert(request: RecipeRequest):
    # Here you’d plug in your existing Python scraper
    
    return {"ingredients": grocery_list}