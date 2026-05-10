from app.schemas.generation import GenerationRequest


def build_video_prompt(data: GenerationRequest) -> str:
    keywords = ", ".join(data.keywords)

    prompt = f"""
You are an expert video content creator.

Generate a complete video script and storyboard.

Video Type: {data.video_type}
Topic: {data.topic}
Keywords: {keywords}
Target Audience: {data.target_audience}
Tone: {data.tone}
Duration: {data.duration}

Return ONLY valid JSON format.

JSON Structure:
{{
  "title": "...",
  "hook": "...",
  "script": "...",
  "cta": "...",
  "scenes": [
    {{
      "scene_number": 1,
      "visual": "...",
      "narration": "...",
      "on_screen_text": "...",
      "transition": "..."
    }}
  ]
}}
"""

    return prompt