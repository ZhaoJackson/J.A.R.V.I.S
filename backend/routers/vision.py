from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ..services.vision_service import VisionService
from ..services.openai_gpt import OpenAIService

router = APIRouter()

class VisionRequest(BaseModel):
    image_data: str
    user_message: str = ""

class VisionResponse(BaseModel):
    activities: List[Dict[str, Any]]
    ai_response: str

@router.post("/analyze", response_model=VisionResponse)
async def analyze_activity(request: VisionRequest):
    try:
        # Initialize services
        vision_service = VisionService()
        openai_service = OpenAIService()
        
        # Process image
        vision_results = vision_service.process_image(request.image_data)
        
        # Generate context from vision results
        activity_context = vision_service.get_activity_context(vision_results["activities"])
        
        # Prepare messages for GPT
        messages = [
            {
                "role": "system",
                "content": "You are JARVIS, a helpful personal assistant that analyzes user activities through computer vision and provides relevant assistance. Be concise and helpful in your responses."
            },
            {
                "role": "user",
                "content": f"{activity_context}\n\nUser message: {request.user_message}"
            }
        ]
        
        # Get AI response
        ai_response = await openai_service.create_chat_completion(messages)
        
        return VisionResponse(
            activities=vision_results["activities"],
            ai_response=ai_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 