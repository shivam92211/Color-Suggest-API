from fastapi import APIRouter, UploadFile, File, Form, HTTPException
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

# Define the endpoint for couple color suggestions
@router.post("/couple-suggestion/")
async def analyze_images(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    occasion: str = Form(...)
):
    try:
        image_data1 = await file1.read()
        image1 = Image.open(io.BytesIO(image_data1))

        image_data2 = await file2.read()
        image2 = Image.open(io.BytesIO(image_data2))

        # prompt = f"""
        # Role: You are an AI stylist and color consultant.

        # Task: Analyze the skin tones of a couple from two provided images (one of a male and one of a female). Based on the analysis, provide detailed clothing color recommendations for each individual. Also, suggest how their outfits can complement each other according to the occasion provided.

        # Format: Your response should be structured in markdown with the following sections:

        # 1. Introduction: Briefly describe the purpose of the analysis and the occasion provided.
        # 2. Individual Recommendations:
        # - Male:
        #     - **Skin Tone**: (e.g., Ivory, Beige, etc.)
        #     - **Recommended Colors**: List and describe suitable clothing colors.
        #     - **Style Suggestions:** Offer styling advice based on the skin tone.
        # - Female:
        #     - **Skin Tone**: (e.g., Fair, Olive, etc.)
        #     - **Recommended Colors**: List and describe suitable clothing colors.
        #     - **Style Suggestions**: Offer styling advice based on the skin tone.
        # 3. Complementary Outfit Suggestions: Provide advice on how the outfits can complement each other, including color coordination and style tips based on the given occasion.
        # 4. Occasion Context: Include a summary of how the recommendations align with the occasion.

        # Input: {occasion}
        # """


        prompt = f"""Role: Fashion AI assistant specializing in skin tone analysis and complementary clothing recommendations.

        Task: Analyze the skin tones of two individuals (one male and one female) from the provided images and provide detailed clothing color and style recommendations. Additionally, suggest how their outfits can complement each other for the given occasion.

        Your Response Format:
        ## Style Analysis and Recommendations for the Occasion: **{{occasion}}**

        ### 1. Introduction
        Provide a brief overview of the purpose of this analysis and how it relates to the given occasion.

        ### 2. Individual Recommendations
        #### Male:
        - **Skin Tone:** {{skin_tone_male}}  
        (e.g., Fair, Olive, Beige, etc.)
        - **Recommended Colors:**  
        - Primary Colors: {{primary_color_male_1}}, {{primary_color_male_2}}, {{primary_color_male_3}}  
        - Accent Colors: {{accent_color_male_1}}, {{accent_color_male_2}}, {{accent_color_male_3}}  
        - **Style Suggestions:**  
        - {{style_tip_male_1}}  
        - {{style_tip_male_2}}  

        #### Female:
        - **Skin Tone:** {{skin_tone_female}}  
        (e.g., Fair, Olive, Beige, etc.)
        - **Recommended Colors:**  
        - Primary Colors: {{primary_color_female_1}}, {{primary_color_female_2}}, {{primary_color_female_3}}  
        - Accent Colors: {{accent_color_female_1}}, {{accent_color_female_2}}, {{accent_color_female_3}}  
        - **Style Suggestions:**  
        - {{style_tip_female_1}}  
        - {{style_tip_female_2}}  

        ### 3. Complementary Outfit Suggestions
        Provide insights into how the male and female outfits can harmonize and enhance each other for the given occasion. Discuss color coordination and style synergy.

        ### 4. Occasion Context
        Summarize how the recommendations align with the occasion's theme and requirements.

        Input: **Occasion**: {occasion}
        """

        response = genai.GenerativeModel("gemini-1.5-flash").generate_content([prompt, image1, image2])
        response.resolve()
        return HTMLResponse(content=response.text)
    except Exception as e:
        logger.error(f"Error in /couple-suggestion/: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
