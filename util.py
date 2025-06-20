import re
from unicodedata import numeric
from fraction import Fraction
import inflect

def to_float(str) -> float:
    """
    Converts numeric string and/or unicode to a float
    """
    if not str:
        raise ValueError(f"Numeric string '{str}' must be a fraction or mixed number")
    sum = 0
    # Considers mixed fraction parts separately
    for s in re.split(r" |([\u00BC-\u00BE\u2150-\u215E])", str, maxsplit=1):
        if not s:
            continue
        try:
            # For normal float representations (ex: '0.5')
            sum += float(s)
            continue
        except ValueError:
            try:
                # For fractional representations (ex: '1/2')
                numerator, denominator = s.split("/")
                sum += float(numerator) / int(denominator)
                continue
            except ValueError:
                try:
                    # For unicode (ex: '½')
                    sum += numeric(s)
                except TypeError:
                    raise ValueError(f"Numeric string '{str}' must be a fraction or mixed number")
    return sum

def to_mixed_num(decimal:float) -> str:
    """Turns decimal into a string mixed number"""
    frac = Fraction(decimal)
    whole = frac.numerator // frac.denominator
    remainder = frac - whole

    if remainder == 0:
        return str(whole)
    elif whole == 0:
        return f"{remainder.numerator}/{remainder.denominator}"
    else:
        return f"{whole} {remainder.numerator}/{remainder.denominator}"
    
def singularize(word):
    """Converts plurals to singular"""
    p = inflect.engine()
    singular = p.singular_noun(word)
    return singular if singular else word

def pluralize(word):
    """Converts singulars to plural"""
    p = inflect.engine()
    plural = p.plural_noun(word)
    return plural if plural else word