from list_manager.util import to_float, to_mixed_num, singularize, is_valid_url
from list_manager.culinary_units import is_valid_unit, UREG
from ingredient_parser import dataclasses, parse_ingredient
from recipe_scrapers import scrape_me
from pint import errors
import inflect

class GroceryList():

    def __init__(self):
        self.items = {}

    def add_link(self, url):
        gl = []
        code = 0
        if not url:
            code = 1 # blank response
        elif not is_valid_url(url):
            code = 2 # not a url
        else:
            try:
                ingredients = scrape_me(url).ingredients()
                for ingredient in ingredients:
                    self.add(ingredient)
                    gl.append(str(ingredient))
            except:
                code = 3 # unable to find recipe
        return {"items" : gl, "code" : code}


    def add_all(self, ingredients):
        """Adds list of ingredients to items dictionary"""
        for ingredient in ingredients:
            self.add(ingredient)
    
    def add(self, ingredient):
        """Adds ingredient to items dictionary, accumulates duplicates iff units are compatible"""
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