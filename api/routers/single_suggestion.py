from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from PIL import Image
import io
import logging
import google.generativeai as genai
import api.genai_config  # Import the genai API configuration

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize the router
router = APIRouter()

# Define the endpoint for color suggestions
@router.post("/single-suggestion/")
async def analyze_image(file: UploadFile = File(...)):
    logger.info("Received request for /single-suggestion/")
    try:
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

        response = genai.GenerativeModel("gemini-1.5-flash").generate_content([prompt, image])
        response.resolve()
        logger.info("AI response generated successfully")
        return HTMLResponse(content=response.text)
    except Exception as e:
        logger.error(f"Error in /color-suggestion/: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
