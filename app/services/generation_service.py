import asyncio
import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.generation import Generation
from app.schemas.generation import GenerationRequest
from app.services.gemini_service import generate_content
from app.utils.prompt_builder import build_video_prompt


async def generate_video_content(
    db: AsyncSession,
    current_user,
    data: GenerationRequest
):
    prompt = build_video_prompt(data)

    try:
        raw_response = await asyncio.wait_for(
            generate_content(prompt),
            timeout=60
        )

        parsed_response = json.loads(raw_response)

        generation = Generation(
            user_id=current_user.id,
            video_type=data.video_type,
            topic=data.topic,
            keywords=",".join(data.keywords),
            target_audience=data.target_audience,
            tone=data.tone,
            duration=data.duration,

            generated_title=parsed_response.get("title"),
            generated_hook=parsed_response.get("hook"),
            generated_script=parsed_response.get("script"),
            generated_cta=parsed_response.get("cta"),

            generated_storyboard=parsed_response.get("scenes"),

            raw_response=parsed_response
        )

        db.add(generation)

        await db.commit()

        await db.refresh(generation)

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