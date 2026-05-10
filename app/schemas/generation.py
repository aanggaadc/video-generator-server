from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    video_type: str
    topic: str
    keywords: List[str]
    target_audience: str
    tone: str

    duration: Optional[str] = "60s"
    number_of_variations: Optional[int] = 1
    template: Optional[str] = None

class SceneSchema(BaseModel):
    scene_number: int
    visual: str
    narration: str
    on_screen_text: str
    transition: str


class GenerationResponse(BaseModel):
    title: str
    hook: str
    script: str
    cta: str

    scenes: List[SceneSchema]


class GenerationHistoryResponse(BaseModel):
    id: str
    video_type: str
    topic: str
    generated_title: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True