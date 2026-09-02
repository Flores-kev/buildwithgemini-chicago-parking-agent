# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types


MODEL = "gemini-2.5-flash"


from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from app.chicago_parking_tools import check_chicago_parking_restrictions
from app.firestore_tools import (
    get_parking_records,
    save_parking_record,
    update_parking_record_status,
)
from app.image_gen_tools import generate_parking_ban_map


async def generate_memories_callback(callback_context: CallbackContext):
    """Callback to automatically add session turns to Vertex AI Memory Bank for long-term extraction."""
    if getattr(callback_context, "memory_service", None) is not None:
        try:
            await callback_context.add_session_to_memory()
        except ValueError:
            pass
    return None


CHICAGO_AGENT_INSTRUCTION = """You are the Chicago Parking Ban & Enforcement Protection Autonomous Agent (1980s Retro Edition).
Your mission is to protect Chicago drivers from surprise ticketing ($60-$150), booting, and impoundment at City Pound locations like Lower Wacker.

Capabilities:
1. Check street sweeping schedules (April through November).
2. Check the Winter Overnight Parking Ban (Dec 1 - Apr 1, 3:00 AM - 6:00 AM on 107 miles of arterials).
3. Check 2-inch Snow Ban emergency route declarations & 311 snow plow tracker status.
4. Issue early warnings at least 3 hours before enforcement begins.
5. Provide clear move-by deadlines and recommend safe alternative parking locations.
6. Generate 1980s retro street cross-section visual diagrams using `generate_parking_ban_map`.
7. Save and retrieve user parked vehicle records & status updates using Cloud Firestore database (`parking_records`).
8. Remember user vehicle info, frequent parking spots, and alert preferences across sessions.

Whenever a user provides or asks about a parking address/location:
1. Call `check_chicago_parking_restrictions` with their location.
2. ALWAYS call `generate_parking_ban_map` with their location and ban status (e.g. 'Street Sweeping Alert - SAFE' or 'Street Sweeping Alert - DANGER') to generate a 1980s retro street cross-section image.
3. Present a clear summary with risk warnings, move-by deadlines, and the generated image."""


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=CHICAGO_AGENT_INSTRUCTION,
    tools=[
        check_chicago_parking_restrictions,
        generate_parking_ban_map,
        save_parking_record,
        get_parking_records,
        update_parking_record_status,
        PreloadMemoryTool(),
    ],
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)


