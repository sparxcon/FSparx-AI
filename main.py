import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import asyncio
import io
import logging
from PIL import Image
import pytesseract
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import re

# Fix Tesseract path for Railway/Nixpacks
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Import secrets
try:
    from secrets import GROQ_API_KEY, DISCORD_TOKEN
except ImportError:
    print("ERROR: secrets.py not found. Please create it with your API keys.")
    exit(1)

# Configuration
ALLOWED_CHANNEL_ID = 1472309916864876596
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds
MOD_ROLE_NAME = "MOD"

# Supported image formats
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".webp"}

# Hardcoded Groq limits (from Groq docs Rate Limits table; Free plan; org-level, may vary by account tier)
GROQ_LIMITS_FREE = {
    "model": "llama-3.3-70b-versatile",
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


async def download_image(url: str) -> bytes:
    """Download image from URL asynchronously"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise Exception(f"Failed to download image: HTTP {response.status}")


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from image using OCR"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")
        # Perform OCR
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR error: {e}")
        raise


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


async def query_groq(question: str) -> str:
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

    user_prompt = (
        f"{question}\n\nReturn only the final answer(s) in the required format; "
        "do not output steps."
    )

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
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
        extracted_text = ""

        # Process image if provided
        if image:
            # Validate image format
            file_ext = Path(image.filename).suffix.lower()
            if file_ext not in SUPPORTED_FORMATS:
                await interaction.followup.send(
                    f"Unsupported image format. Please use: "
                    f"{', '.join(SUPPORTED_FORMATS)}",
                    ephemeral=True,
                )
                return

            try:
                logger.info(f"Downloading image: {image.filename}")
                image_bytes = await download_image(image.url)
                logger.info("Extracting text from image...")
                extracted_text = extract_text_from_image(image_bytes)
                extracted_text = sanitize_text(extracted_text)
                logger.info(f"Extracted text: {extracted_text[:100]}...")
            except Exception as e:
                logger.error(f"Image processing error: {e}")
                await interaction.followup.send(
                    "Failed to process the image. Please try again with a clearer image.",
                    ephemeral=True,
                )
                return

        # Combine question and extracted text
        combined_text = ""
        if question:
            combined_text = question
        if extracted_text:
            combined_text = f"{combined_text}\n{extracted_text}".strip()

        # Check if we have any content
        if not combined_text:
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True,
            )
            return

        # Check if it's a Sparx-style math question
        if not is_math_question(combined_text):
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True,
            )
            return

        # Query Groq API
        logger.info("Querying Groq API...")
        answer = await query_groq(combined_text)

        # Check if Groq rejected the input
        if answer == "Please upload a question to solve":
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True,
            )
            return

        # --------- Public embed includes user + prompt ---------
        # Truncate combined_text to avoid overly large embeds
        prompt_preview = combined_text
        max_prompt_len = 512
        if len(prompt_preview) > max_prompt_len:
            prompt_preview = prompt_preview[: max_prompt_len - 3] + "..."

        embed = discord.Embed(
            description=answer,
            color=discord.Color.blue(),
            timestamp=datetime.utcnow(),
        )

        # Show the user who triggered it
        embed.set_author(
            name=f"FSparx AI • Requested by {interaction.user}",
            icon_url=getattr(
                interaction.user.display_avatar, "url", discord.Embed.Empty
            ),
        )

        # Add the prompt (text and/or OCR result)
        embed.add_field(
            name="Prompt",
            value=prompt_preview or "*No text extracted*",
            inline=False,
        )

        # Note if there was an image
        if image:
            embed.add_field(
                name="Source",
                value="Text + Image" if question else "Image only",
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
        timestamp=datetime.utcnow(),
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
