import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import re

# Import config
try:
    from config import GROQ_API_KEY, DISCORD_TOKEN
except ImportError:
    print("ERROR: config.py not found. Please create it with your API keys.")
    exit(1)

# Configuration
ALLOWED_CHANNEL_ID = 1472309916864876596
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Use a vision model when an image is provided
GROQ_VISION_MODEL = "llama-3.2-90b-vision-preview"
# Use a text-only model for text queries
GROQ_TEXT_MODEL = "llama-3.3-70b-versatile"

RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds
MOD_ROLE_NAME = "MOD"

# Supported image formats
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".webp"}

# Hardcoded Groq limits (from Groq docs Rate Limits table; Free plan; org-level, may vary by account tier)
GROQ_LIMITS_FREE = {
    "model": GROQ_TEXT_MODEL,
    "rpm": 30,
    "rpd": 1000,
    "tpm": 12000,
    "tpd": 100000,
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("discord_bot")

# Rate limiting storage
user_requests = defaultdict(list)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def check_rate_limit(user_id: int, has_mod_role: bool) -> tuple[bool, int]:
    """
    Check if user has exceeded rate limit.
    Returns (is_allowed, remaining_requests)
    """
    if has_mod_role:
        return True, -1  # Unlimited for mods

    now = datetime.now()
    cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW)

    # Clean old requests
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id] if req_time > cutoff
    ]
    current_count = len(user_requests[user_id])

    if current_count >= RATE_LIMIT_REQUESTS:
        return False, 0

    user_requests[user_id].append(now)
    return True, RATE_LIMIT_REQUESTS - current_count - 1


def has_mod_role(interaction: discord.Interaction) -> bool:
    """Check if user has MOD role"""
    if not interaction.guild or not interaction.user:
        return False

    member = interaction.user
    if isinstance(member, discord.Member):
        return any(role.name.upper() == MOD_ROLE_NAME.upper() for role in member.roles)

    return False


def is_math_question(text: str) -> bool:
    """
    Basic heuristic to detect if text contains math-like content.
    (Kept the same logic – Sparx questions are still math-y.)
    """
    if not text or len(text.strip()) < 3:
        return False

    # Check for math indicators
    math_patterns = [
        r"\d+",  # Numbers
        r"[+\-\\*/=<>]",  # Operators
        r"\b(solve|find|calculate|compute|evaluate|simplify|prove)\b",  # Math verbs
        r"\b(equation|function|derivative|integral|limit|sum|product)\b",  # Math terms
        r"[xyz][\s]\*=",  # Variables
        r"\^|\\*\\*",  # Exponents
    ]

    for pattern in math_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def sanitize_text(text: str) -> str:
    """Remove UI artifacts and clean text"""
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove common UI artifacts
    text = re.sub(r"[▪•◦▫]", "", text)
    return text.strip()


async def query_groq(question: str | None, image_url: str | None) -> str:
    """
    Query Groq API asynchronously with retry logic.
    Returns the model's response text.
    """
    system_prompt = (
        "You are a Sparx question solver. The user will send questions copied from "
        "Sparx Maths or screenshots of Sparx questions.\n\n"
        "If the input is not a valid Sparx-style maths question or is empty/irrelevant, "
        "reply exactly: 'Please upload a question to solve'.\n\n"
        "If the input is a Sparx question, produce ONLY the final answer(s) with NO WORKINGS. "
        "Format the answer exactly as described: start with '# ' at the very beginning, "
        "then either '# Answer = ' or '# Answers:' followed by newline-separated "
        "'a = ' lines for multiple values. Do not include any additional text, "
        "context, or reasoning."
    )

    if image_url:
        model = GROQ_VISION_MODEL
        content_parts = []
        if question and question.strip():
            content_parts.append({"type": "text", "text": question})
        else:
            content_parts.append({"type": "text", "text": "Solve the math problem in the image."})
        content_parts.append({"type": "image_url", "image_url": {"url": image_url}})

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content_parts},
        ]
    else:
        model = GROQ_TEXT_MODEL
        user_prompt = (
            f"{question}\n\nReturn only the final answer(s) in the required format; "
            "do not output steps."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 500,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    max_retries = 3

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    GROQ_API_URL,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        answer = data["choices"][0]["message"]["content"].strip()
                        return answer
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"Groq API error (attempt {attempt + 1}): "
                            f"{response.status} - {error_text}"
                        )

            if attempt < max_retries - 1:
                await asyncio.sleep(2**attempt)  # Exponential backoff
            else:
                raise Exception(f"Groq API failed after {max_retries} attempts")

        except asyncio.TimeoutError:
            logger.error(f"Groq API timeout (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                await asyncio.sleep(2**attempt)
            else:
                raise Exception("Groq API timeout")
        except Exception as e:
            logger.error(f"Groq API exception (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2**attempt)
            else:
                raise


@bot.event
async def on_ready():
    """Bot startup event"""
    logger.info(f"Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")


@bot.tree.command(
    name="solve",
    description="Solve a Sparx question from text or image",
)
@app_commands.describe(
    question="The Sparx question to solve (optional if image provided)",
    image="Image containing the Sparx question (optional if question provided)",
)
async def solve(
    interaction: discord.Interaction,
    question: str | None = None,
    image: discord.Attachment | None = None,
):
    """Main /solve command handler"""
    # Check if command is in allowed channel
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            "Please use #question-ai for automated Sparx question solving",
            ephemeral=True,
        )
        return

    # Check rate limit
    is_mod = has_mod_role(interaction)
    allowed, remaining = check_rate_limit(interaction.user.id, is_mod)
    if not allowed:
        await interaction.response.send_message(
            "You have reached your rate limit of 10 requests per hour. "
            "Please try again later.",
            ephemeral=True,
        )
        return

    # Send ephemeral "Working..." message
    await interaction.response.send_message("Working...", ephemeral=True)

    try:
        # Validate image format if provided
        if image:
            file_ext = Path(image.filename).suffix.lower()
            if file_ext not in SUPPORTED_FORMATS:
                await interaction.followup.send(
                    f"Unsupported image format. Please use: "
                    f"{', '.join(SUPPORTED_FORMATS)}",
                    ephemeral=True,
                )
                return

        # Clean text prompt
        clean_question = sanitize_text(question) if question else None

        # If no text and no image, stop
        if not clean_question and not image:
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True,
            )
            return

        # If text-only, enforce math check
        if clean_question and not image and not is_math_question(clean_question):
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True,
            )
            return

        # Query Groq API (image sent directly when provided)
        logger.info("Querying Groq API...")
        answer = await query_groq(clean_question, image.url if image else None)

        # Check if Groq rejected the input
        if answer == "Please upload a question to solve":
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True,
            )
            return

        # --------- Public embed includes user + prompt ---------
        # Truncate prompt to avoid overly large embeds
        prompt_preview = clean_question or "*Image only*"
        max_prompt_len = 512
        if len(prompt_preview) > max_prompt_len:
            prompt_preview = prompt_preview[: max_prompt_len - 3] + "..."

        embed = discord.Embed(
            description=answer,
            color=discord.Color.blue(),
            timestamp=datetime.now(timezone.utc),
        )

        # Show the user who triggered it
        embed.set_author(
            name=f"FSparx AI • Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url if interaction.user.display_avatar else None,
        )

        # Add the prompt (text and/or image)
        embed.add_field(
            name="Prompt",
            value=prompt_preview,
            inline=False,
        )

        # Note if there was an image
        if image:
            embed.add_field(
                name="Source",
                value="Text + Image" if clean_question else "Image only",
                inline=True,
            )
        else:
            embed.add_field(
                name="Source",
                value="Text only",
                inline=True,
            )

        # Send public message in channel so everyone can see it
        await interaction.channel.send(embed=embed)
        # -------------------------------------------------------

        # Update ephemeral message
        rate_limit_msg = (
            "" if is_mod else f"\n\nYou have {remaining} requests remaining this hour."
        )
        await interaction.edit_original_response(
            content=f"✅ Answer posted!{rate_limit_msg}"
        )
        logger.info(f"Successfully processed request from {interaction.user}")
    except Exception as e:
        logger.error(f"Unexpected error in solve command: {e}", exc_info=True)
        try:
            await interaction.followup.send(
                "An error occurred while processing your request.",
                ephemeral=True,
            )
        except Exception:
            pass


@bot.tree.command(name="info", description="How to use FSparx AI + rate limits")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="FSparx AI • Info",
        description=(
            "FSparx AI is a **Sparx solver**.\n"
            "Paste Sparx questions or upload Sparx screenshots, and the bot "
            "returns only the **final answer** in a public embed.\n\n"
            "Bot made and hosted by **@uh.izaak**."
        ),
        color=discord.Color.blue(),
        timestamp=datetime.now(timezone.utc),
    )

    embed.add_field(
        name="How to use",
        value=(
            f"Use `/solve` in <#{ALLOWED_CHANNEL_ID}>.\n"
            "• Text: `/solve question: `\n"
            "• Image: `/solve image: `\n"
            "• Both: provide text + image in the same command\n\n"
            "The bot posts the answer **publicly** in the channel."
        ),
        inline=False,
    )

    embed.add_field(
        name="Rate limits",
        value=(
            f"• Per-person: **{RATE_LIMIT_REQUESTS} requests per hour** "
            f"(Role `{MOD_ROLE_NAME}`: unlimited)\n"
            f"• Groq (Free plan) for `{GROQ_LIMITS_FREE['model']}`: "
            f"**{GROQ_LIMITS_FREE['rpm']} RPM**, **{GROQ_LIMITS_FREE['rpd']} RPD**, "
            f"**{GROQ_LIMITS_FREE['tpm']} TPM**, **{GROQ_LIMITS_FREE['tpd']} TPD**\n\n"
            "Groq limits are **org-level** and may vary by account tier."
        ),
        inline=False,
    )

    # Public (visible to everyone)
    await interaction.response.send_message(embed=embed, ephemeral=False)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
