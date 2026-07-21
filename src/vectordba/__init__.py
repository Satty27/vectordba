# 1. Explicitly import the functions from your internal modules
from .core import VectorAgent
import os
from dotenv import load_dotenv


current_path = os.getcwd()
print(f"DEBUG: Looking for .env file in: {current_path}")
from dotenv import find_dotenv
found_path = find_dotenv(usecwd=True)
print(f"DEBUG: Auto-discovered .env path: {found_path}")

load_dotenv(dotenv_path=found_path, override=True)
__version__ = "0.1.1"

__all__ = ["VectorAgent"]