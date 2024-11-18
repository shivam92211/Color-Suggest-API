import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize logger
logger = logging.getLogger(__name__)

if not api_key:
    logger.error("GOOGLE_API_KEY not found. Please set the API key in the .env file or environment.")
    raise EnvironmentError("GOOGLE_API_KEY is missing")
else:
    # Configure the API with the key
    genai.configure(api_key=api_key)
    logger.info("Generative AI API key successfully configured.")
