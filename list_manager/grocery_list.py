from list_manager.util import to_float, to_mixed_num, singularize, is_valid_url
from list_manager.culinary_units import is_valid_unit, UREG
from ingredient_parser import dataclasses, parse_ingredient
from recipe_scrapers import scrape_me
from pint import errors
import inflect

class UrlError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        
class GroceryList():

    def __init__(self):
        self.items = {}

    def search_link(self, url):
        try:
            return Recipe(url), 200 # success
        except UrlError as e:
            return None, e.status_code

    def add_all(self, ingredients):
        """Adds list of ingredients to items dictionary"""
        for ingredient in ingredients:
            self.add(ingredient)
    
    def add(self, ingredient):
        """Adds ingredient to items dictionary, accumulates duplicates iff units are compatible"""
        if not isinstance(ingredient, Ingredient):
            ingredient = Ingredient(parse_ingredient(ingredient))
        name = ingredient.title
        while True:
            if name not in self.items.keys():
                self.items[name] = ingredient
                break
            else:
                try:
                    self.items[name] += ingredient
                    break
                except errors.DimensionalityError:
                    # If units are noncompatible, create new key
                    # (ex: 2 cups strawberries vs 1 strawberry)
                    ingredient.title = name + u"\u200b"
                    name = ingredient.title
                
    def get_items(self):
        gl = []
        for item in self.items.keys():
            gl.append(str(self.items[item]))
        return gl
    
    def get_ingredients(self):
        gl = []
        for item in self.items.keys():
            gl.append(self.items[item])
        return gl

    def __str__(self):
        """Converts GroceryList to printable"""
        print("---------------------\nGrocery List \n---------------------")
        gl = ""
        if len(self.items) > 0:
            for item in self.items.keys():
                gl += f"{self.items[item]}\n"
            return gl
        else:
            return "Empty List"
class Recipe():
    def __init__(self, url):
        if not url:
            raise UrlError("Url is blank", 422)
        elif not is_valid_url(url):
            raise UrlError("Invalid url", 400)
        
        try:
            self._json = scrape_me(url).to_json()
        except Exception:
            raise UrlError("Unable to find recipe", 404)
        
        self.title = self._json["title"]
        self._ingredients = self.get_ingredients()
        self._yields = int(self._json["yields"].split(" ")[0])

        self.scaled_ingredients = self._ingredients
        self.servings = self._yields
    
    def get_ingredients(self):
        ingredient_list = []
        for ingredient in self._json["ingredients"]:
            ingredient_list.append(Ingredient(parse_ingredient(ingredient)))
        return ingredient_list
    
    def scale(self, multiplier):
        for ingredient in self.scaled_ingredients:
            ingredient = self._base_ingredients * multiplier
        self.servings *= multiplier
    
    def to_json(self):
        json = {
            "title": self.title,
            "ingredients": [],
            "yields": self._yields,
            "servings": self.servings
        }
        # turn into string list
        for ingredient in self.scaled_ingredients:
            json["ingredients"].append(str(ingredient))
        return json
        
class Ingredient(dataclasses.ParsedIngredient):
    def __init__(self, i):
        super().__init__(i.name, i.size, i.amount, i.preparation, i.comment, 
                         i.purpose, i.foundation_foods, i.sentence)
        self.quantity = self.quantify()
        self.title = singularize(self.name[0].text.lower())
    
    def quantify(self):
        if len(self.amount) > 0:
            amt = self.amount[0]
            try:
                q = to_float(str(self.amount[0].quantity))
            except TypeError: 
                q = 1 # amount cannot be parsed
            unit = amt.unit if is_valid_unit(amt.unit) else 'count'
        else:
            q = 1.0
            unit = 'count'
        return UREG.Quantity(q, unit)
    
    def __add__(self, other):
        if isinstance(other, Ingredient):
            return self.quantity + other.quantity
        else:
            raise TypeError(f"unsupported operand type(s) for + 'Ingredient' and {type(other)}")
        
        
    def __iadd__(self, other):
        if isinstance(other, Ingredient):
            self.quantity += other.quantity
            return self
        else:
            raise TypeError(f"unsupported operand type(s) for + 'Ingredient' and {type(other)}")
        
    def __mul__(self, other):
        if isinstance(other, float):
            return self.quantity * other.quantity
        else:
            raise TypeError(f"unsupported operand type(s) for + 'Ingredient' and {type(other)}")
        
        
    def __imul__(self, other):
        if isinstance(other, float):
            self.quantity *= other.quantity
            return self
        else:
            raise TypeError(f"unsupported operand type(s) for + 'Ingredient' and {type(other)}")
    
    def __str__(self):
        """Converts Ingredient to string"""
        p = inflect.engine()
        amount = self.quantity.magnitude
        if self.quantity.units != UREG.dimensionless:
            if amount > 1:
                # ex: "4 cloves of garlic"
                unit = p.plural_noun(str(self.quantity.units), amount)
            else:
                # ex: "1/2 cup of flour"
                unit = str(self.quantity.units)
            return f"{to_mixed_num(amount)} {unit} of {self.title}"
        else:
            # No units (ex: "1 strawberry" | "2 oranges")
            item = p.plural_noun(self.title, self.quantity.magnitude)
            return f"{to_mixed_num(amount)} {item}"