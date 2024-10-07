from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Allow CORS for all origins (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the generative AI model
genai.configure(api_key=api_key)
image_model = genai.GenerativeModel("gemini-1.5-flash")


@app.post("/color-suggestion/")
async def analyze_image(file: UploadFile = File(...)):
    logger.info("Received request for /color-suggestion/")
    try:
        # Read the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        logger.info("Image opened successfully")

        prompt = """
        Role: Fashion AI assistant with expertise in analyzing skin tones and recommending complementary clothing colors.
        
        Task: 
        1. Analyze the provided photo of a person.
        2. Determine the skin shade of the individual.
        3. Based on the detected skin shade, suggest the most suitable clothing colors.
        4. If multiple people are detected in the image, respond with:
           "Cannot suggest since multiple persons are detected."
        5. If no person is found in the image, respond with:
           "Sorry, no person found."
        
        Your Response Format:
        ## Skin Tone Analysis and Clothing Recommendations

        **Skin Shade Detected:** {{skin_shade}}

        ### Clothing Color Recommendations:
        Based on the detected skin shade of **{{skin_shade}}**, here are the recommended clothing colors:

        - **Primary Colors:** 
          - {{primary_color_1}}
          - {{primary_color_2}}
          - {{primary_color_3}}

        - **Accent Colors:**
          - {{accent_color_1}}
          - {{accent_color_2}}
          - {{accent_color_3}}

        ### Style Tips:
        - For a casual look, consider wearing {{suggested_outfit_1}}.
        - For a formal look, {{suggested_outfit_2}} would be ideal.
        - Accessories in {{accessory_color}} would provide a great finishing touch.
        """

        # Generate response from the AI model
        logger.info("Generating content with AI model")
        response = image_model.generate_content([prompt, image])
        response.resolve()
        logger.info("AI response generated successfully")
        return HTMLResponse(content=response.text)
    except Exception as e:
        logger.error(f"Error in /color-suggestion/: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/color-suggestion-couple/")
async def analyze_images(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    occasion: str = Form(...)
):
    # Read and open the uploaded images
    image_data1 = await file1.read()
    image1 = Image.open(io.BytesIO(image_data1))

    image_data2 = await file2.read()
    image2 = Image.open(io.BytesIO(image_data2))

    prompt = f"""
    Role: You are an AI stylist and color consultant.

    Task: Analyze the skin tones of a couple from two provided images (one of a male and one of a female). Based on the analysis, provide detailed clothing color recommendations for each individual. Also, suggest how their outfits can complement each other according to the occasion provided.

    Format: Your response should be structured in markdown with the following sections:

    1. Introduction: Briefly describe the purpose of the analysis and the occasion provided.
    2. Individual Recommendations:
    - Male:
        - Skin Tone: (e.g., Ivory, Beige, etc.)
        - Recommended Colors: List and describe suitable clothing colors.
        - Style Suggestions: Offer styling advice based on the skin tone.
    - Female:
        - Skin Tone: (e.g., Fair, Olive, etc.)
        - Recommended Colors: List and describe suitable clothing colors.
        - Style Suggestions: Offer styling advice based on the skin tone.
    3. Complementary Outfit Suggestions: Provide advice on how the outfits can complement each other, including color coordination and style tips based on the given occasion.
    4. Occasion Context: Include a summary of how the recommendations align with the occasion.

    Input: {occasion}
    """

    try:
        # Generate response from the AI model
        response = image_model.generate_content([prompt, image1, image2])
        response.resolve()
        return HTMLResponse(content=response.text)
    except Exception as e:
        return {"error": str(e)}

