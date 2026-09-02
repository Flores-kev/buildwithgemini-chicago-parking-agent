"""Image generation tool for Chicago parking restriction map visualizations.

Uses gemini-3.1-flash-lite-image in the global region.
Saves the generated image as an artifact via ToolContext and uploads to public Cloud Storage bucket.
"""

import datetime
from typing import Any

from google import genai
from google.adk.tools.tool_context import ToolContext
from google.cloud import storage
from google.genai import types

PROJECT_ID = "qwiklabs-gcp-03-1a24275fdf4b"
BUCKET_NAME = "bwg3-qwiklabs-gcp-03-1a24275fdf4b"
MODEL_NAME = "gemini-3.1-flash-lite-image"


async def generate_parking_ban_map(
    location: str,
    ban_type: str = "Street Sweeping Alert",
    tool_context: ToolContext | None = None,
) -> dict[str, Any]:
    """Generates a visual map/warning image for a Chicago parking ban location using gemini-3.1-flash-lite-image.

    Saves the image into the agent Playground Artifacts panel and uploads it to Cloud Storage.

    Args:
        location: The Chicago street address or intersection (e.g. '1200 N Milwaukee Ave').
        ban_type: The type of parking restriction (e.g. 'Street Sweeping Alert', 'Winter Overnight Ban', '2-Inch Snow Ban').
        tool_context: Optional ADK ToolContext for saving session artifacts.

    Returns:
        A dictionary containing the status, location, ban_type, and public GCS HTTPS URL.
    """
    prompt = (
        f"A 1980s retro Memphis-style architectural street cross-section diagram of a Chicago street zone at '{location}'. "
        f"Restriction Status: '{ban_type}'. "
        f"Features a cross-section showing sidewalk, curb, parked vehicle, roadway lanes, clear Chicago parking restriction signs, "
        f"bold neon 80s status badges (glowing green SAFE or glowing red DANGER zone indicators), synthwave grid lines, "
        f"and vibrant 1980s magenta, cyan, and purple colors."
    )

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    image_bytes = None
    mime_type = "image/png"

    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                if part.inline_data.mime_type:
                    mime_type = part.inline_data.mime_type
                break

    if not image_bytes:
        return {
            "status": "ERROR",
            "message": "Failed to generate image bytes from model response.",
        }

    timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    extension = "png" if "png" in mime_type else "jpg"
    filename = f"parking_map_{timestamp}.{extension}"

    # 1. Save as ADK artifact for Playground UI
    if tool_context:
        artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        await tool_context.save_artifact(filename=filename, artifact=artifact_part)

    # 2. Upload to public Cloud Storage bucket
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    return {
        "status": "SUCCESS",
        "location": location,
        "ban_type": ban_type,
        "public_url": public_url,
        "filename": filename,
        "message": f"Successfully generated parking map visualization for {location}",
    }
