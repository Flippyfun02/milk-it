from ingredient_parser._common import UREG
from pint import errors, Unit

defined_units = {
    'clove', 'leaf', 'bunch', 'sprig', 'stalk', 'head', 'bulb', 'ear',
    'slice', 'piece', 'fillet', 'steak', 'cutlet', 'drumstick', 'wing',
    'can', 'jar', 'bottle', 'packet', 'box', 'container', 'bag', 'bar', 'stick',
    'skewer', 'cube', 'ball', 'sheet', 'round', 'wheel', 'log', 'roll',
    'rib', 'strip', 'drop', 'pinch', 'dash'
}

for unit in defined_units:
    UREG.define(f"{unit} = [count]")

def define(unit):
    if unit not in defined_units:
        try:
            UREG.define(f"{unit} = [count]")
            defined_units.add(unit)
        except ValueError:
            # already defined
            return 0
    return 1

def is_valid_unit(unit):
    """Determines if a unit valid and defines it if not in UnitRegistry"""
    if isinstance(unit, Unit):
        return True
    try:
        _ = 1 * UREG(unit)
        return True
    except errors.UndefinedUnitError:
        # Assumes if it uses language of a pint.Unit, it is valid
        if any(u in defined_units for u in unit) or any(u in UREG for u in unit):
            UREG.define(f"{unit} = [count]")
        return False