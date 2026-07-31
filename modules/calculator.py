"""Calculator and unit converter"""
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

class Calculator:
    @staticmethod
    def evaluate(expression: str) -> str:
        try:
            # Safe eval - only allow math
            allowed = {"__builtins__": {}}
            import math
            allowed.update({k: getattr(math, k) for k in dir(math) if not k.startswith('_')})
            result = eval(expression, allowed)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {e}"

    @staticmethod
    def convert_currency(amount: float, from_curr: str, to_curr: str) -> str:
        try:
            import requests
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr.upper()}"
            r = requests.get(url, timeout=10)
            data = r.json()
            rate = data["rates"].get(to_curr.upper())
            if rate:
                return f"{amount} {from_curr.upper()} = {amount * rate:.2f} {to_curr.upper()}"
            return "Currency not found"
        except Exception as e:
            return f"Currency error: {e}"

    @staticmethod
    def convert_unit(value: float, from_unit: str, to_unit: str) -> str:
        conversions = {
            ("km", "mile"): 0.621371, ("mile", "km"): 1.60934,
            ("kg", "lb"): 2.20462, ("lb", "kg"): 0.453592,
            ("cm", "inch"): 0.393701, ("inch", "cm"): 2.54,
            ("celsius", "fahrenheit"): lambda c: c * 9/5 + 32,
            ("fahrenheit", "celsius"): lambda f: (f - 32) * 5/9,
        }
        key = (from_unit.lower(), to_unit.lower())
        if key in conversions:
            factor = conversions[key]
            result = factor(value) if callable(factor) else value * factor
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        return "Conversion not supported"
