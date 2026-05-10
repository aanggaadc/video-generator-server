import json
from app.models.generation import Generation


def build_txt_export(generation: Generation) -> str:
    lines = []

    lines.append(f"Title: {generation.generated_title}\n")

    lines.append("HOOK")
    lines.append(generation.generated_hook or "")
    lines.append("")

    lines.append("SCRIPT")
    lines.append(generation.generated_script or "")
    lines.append("")

    lines.append("CTA")
    lines.append(generation.generated_cta or "")
    lines.append("")

    lines.append("STORYBOARD")

    storyboard = generation.generated_storyboard or []

    for scene in storyboard:
        lines.append(f"\nScene {scene.get('scene_number')}")

        lines.append(
            f"Visual: {scene.get('visual', '')}"
        )

        lines.append(
            f"Narration: {scene.get('narration', '')}"
        )

        lines.append(
            f"On Screen Text: {scene.get('on_screen_text', '')}"
        )

        lines.append(
            f"Transition: {scene.get('transition', '')}"
        )

    return "\n".join(lines)


def build_json_export(generation: Generation) -> str:
    data = {
        "title": generation.generated_title,
        "hook": generation.generated_hook,
        "script": generation.generated_script,
        "cta": generation.generated_cta,
        "scenes": generation.generated_storyboard,
    }

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )