import asyncio
import json

from app.schemas.generation import GenerationRequest
from app.services.gemini_service import generate_content
from app.utils.prompt_builder import build_video_prompt


async def generate_video_content(data: GenerationRequest):
    prompt = build_video_prompt(data)

    try:
        raw_response = await asyncio.wait_for(
            generate_content(prompt),
            timeout=60
        )

        parsed_response = json.loads(raw_response)

        return parsed_response

    except asyncio.TimeoutError:
        return {
            "success": False,
            "message": "AI generation timeout"
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "Invalid AI JSON response",
            "raw_response": raw_response
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }