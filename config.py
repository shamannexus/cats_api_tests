import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CAT_API_KEY")
BASE_URL = "https://api.thecatapi.com/v1"
HEADERS = {"x-api-key": API_KEY}
