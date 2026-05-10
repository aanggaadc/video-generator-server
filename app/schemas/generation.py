from typing import List, Optional

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