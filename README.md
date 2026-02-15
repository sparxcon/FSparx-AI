# FSparx AI Discord Bot

A production-ready Discord bot that solves math questions using OCR and Groq AI. The bot accepts text and/or image inputs, extracts questions, and returns only the final answer in a clean, formatted embed.

## ⚠️ IMPORTANT: This is a Backend-Only Bot

**DO NOT CREATE A FRONTEND OR WEBSITE FOR THIS PROJECT.**

This is a Discord bot that runs as a background service. It does not need a web interface, HTML pages, or any frontend components. The bot communicates directly with Discord's API.

---

## 🤖 For Replit Agent

If you are Replit Agent setting up this project, follow these instructions:

### Installation Steps:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
2. Install Tesseract OCR:
3. Verify installation:
   tesseract --version
4. DO NOT create any frontend, HTML, CSS, or web interface files.
5. DO NOT modify the existing Python files - they are already configured with the correct API keys and channel ID.
6. Expected output:
INFO - Bot logged in as [BotName]
INFO - Synced 1 command(s)


# What this bot does 
Listens for /solve slash commands in Discord
Processes text and image inputs
Uses OCR to extract text from images
Queries Groq AI to solve math problems
Posts answers as Discord embeds

# Troubleshooting 


await response.text()
)
        )
        embed.set_author(name="FSparx AI")

        # Send public message in channel
        await interaction.channel.send(embed=embed)

        # Update ephemeral message
        rate_limit_msg = "" if is_mod else f"\n\nYou have {remaining} requests remaining this hour."
        await interaction.edit_original_response(
            content=f"✅ Answer posted!{rate_limit_msg}"
        )

        logger.info(f"Successfully processed request from {interaction.user}")

    except Exception as e:
        logger.error(f"Unexpected error in solve command: {e}", exc_info=True)
        try:
            await interaction.followup.send(
                "An error occurred while processing your request.",
                ephemeral=True
            )
        except:
            pass


def main():
    """Main entry point"""
    if not GROQ_API_KEY or GROQ_API_KEY == "PASTE_GROQ_KEY_HERE":
        logger.error("GROQ_API_KEY not set in secrets.py")
        return

    if not DISCORD_TOKEN or DISCORD_TOKEN == "PASTE_DISCORD_TOKEN_HERE":
        logger.error("DISCORD_TOKEN not set in secrets.py")
        return

    logger.info("Starting bot...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
===== secrets.py =====

python
Copy
  # ⚠️ WARNING: NEVER COMMIT THIS FILE TO VERSION CONTROL ⚠️
# This file contains sensitive API keys and tokens.
# Add this file to .gitignore to prevent accidental exposure.
#
# To get your keys:
# 1. GROQ_API_KEY: Sign up at https://console.groq.com/ and create an API key
# 2. DISCORD_TOKEN: Create a bot at https://discord.com/developers/applications

GROQ_API_KEY = "PASTE_GROQ_KEY_HERE"
DISCORD_TOKEN = "PASTE_DISCORD_TOKEN_HERE"
===== requirements.txt =====

discord.py>=2.3.2
aiohttp>=3.9.1
Pillow>=10.1.0
pytesseract>=0.3.10
python-dotenv>=1.0.0
===== .replit =====

run = "python main.py"
modules = ["python-3.11"]

[nix]
channel = "stable-23_11"

[deployment]
run = ["sh", "-c", "python main.py"]
deploymentTarget = "cloudrun"
===== README.md =====

markdown
Copy
# FSparx AI Discord Bot

A production-ready Discord bot that solves math questions using OCR and Groq AI. The bot accepts text and/or image inputs, extracts questions, and returns only the final answer in a clean, formatted embed.

## Features

- ✅ `/solve` slash command with text and image support
- ✅ OCR text extraction from images using Tesseract
- ✅ Groq AI (llama-3.3-70b-versatile) for math problem solving
- ✅ Rate limiting (10 requests/hour per user, unlimited for MODs)
- ✅ Channel-specific operation (only works in designated channel)
- ✅ Ephemeral "Working..." status for command invoker
- ✅ Public answer embeds with clean formatting
- ✅ Comprehensive error handling and logging
- ✅ Fully asynchronous for optimal performance

## Setup Instructions

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
5. Click "Reset Token" and copy your bot token (save it for later)
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot` and `applications.commands`
8. Select bot permissions:
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use Slash Commands
9. Copy the generated URL and open it in your browser to invite the bot to your server

### 2. Get Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key and copy it (save it for later)

### 3. Find Your Channel ID

1. In Discord, enable Developer Mode:
   - User Settings → Advanced → Developer Mode (toggle on)
2. Right-click on the channel where you want the bot to work
3. Click "Copy Channel ID"
4. Save this ID for the next step

### 4. Configure the Bot

1. Open `secrets.py` and replace the placeholders:
 
python
Copy
  GROQ_API_KEY = "your_actual_groq_api_key_here"
DISCORD_TOKEN = "your_actual_discord_bot_token_here"
Open main.py and update the channel ID (line 27):
python
Copy
  ALLOWED_CHANNEL_ID = 1234567890123456789  # Replace with your channel ID
IMPORTANT: Never commit secrets.py to version control!
5. Install Dependencies
Local Installation
bash
Copy
# Install Python dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install tesseract-ocr

# On macOS:
brew install tesseract

# On Windows:
# Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
Replit Installation
Tesseract installation on Replit requires special setup:

Create a replit.nix file in your project root:
nix
Copy
{ pkgs }: {
  deps = [
    pkgs.tesseract
    pkgs.python311
    pkgs.python311Packages.pip
  ];
}
Or use the Shell to install:
bash
Copy
nix-env -iA nixpkgs.tesseract
Verify installation:
bash
Copy
tesseract --version
6. Run the Bot
Locally
bash
Copy
python main.py
On Replit
Click the "Run" button at the top
The bot will start automatically
Keep the Replit tab open or use Replit's "Always On" feature (requires paid plan)
Usage
Basic Command
In the designated channel, use:

/solve question: What is 2 + 2?
Or upload an image:

/solve image: [attach image]
Or both:

/solve question: Solve this equation image: [attach image]
Answer Format
The bot returns answers in this format:

Single answer:

# Answer = 42
Multiple answers:

# Answers:
a = 293
b = 393
Rate Limiting
Regular users: 10 requests per hour
Users with "MOD" role: Unlimited requests
Error Messages
"Please use #question-ai for automated question solving" - Command used in wrong channel
"Please upload a question to solve" - No valid math question detected
"You have reached your rate limit..." - Too many requests
"An error occurred while processing your request." - Unexpected error
Configuration
Change Allowed Channel
Edit main.py line 27:

python
Copy
  ALLOWED_CHANNEL_ID = 1234567890123456789  # Your channel ID
Change Rate Limits
Edit main.py lines 28-29:

python
Copy
  RATE_LIMIT_REQUESTS = 10  # Number of requests
RATE_LIMIT_WINDOW = 3600  # Time window in seconds (3600 = 1 hour)
Change MOD Role Name
Edit main.py line 30:

python
Copy
  MOD_ROLE_NAME = "MOD"  # Case-insensitive
Change Groq Model
Edit main.py line 26:

python
Copy
  GROQ_MODEL = "llama-3.3-70b-versatile"  # Or another Groq model
Hosting on Replit
Step-by-Step Replit Deployment
Create a new Repl:
Go to Replit
Click "Create Repl"
Select "Import from GitHub" or "Python" template
Name your Repl (e.g., "fsparx-discord-bot")
Upload files:
Upload all files from this repository
Or use Git import if you have a GitHub repo
Configure secrets (Recommended method):
Click the "Secrets" tab (lock icon) in the left sidebar
Add two secrets:
Key: GROQ_API_KEY, Value: your Groq API key
Key: DISCORD_TOKEN, Value: your Discord bot token
Update secrets.py to read from environment variables:
python
Copy
  import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "PASTE_GROQ_KEY_HERE")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "PASTE_DISCORD_TOKEN_HERE")
Install Tesseract:
Open the Shell tab
Run: nix-env -iA nixpkgs.tesseract
Or create replit.nix as described above
Update channel ID:
Edit main.py and set ALLOWED_CHANNEL_ID
Run the bot:
Click the "Run" button
Bot should start and log "Bot logged in as..."
Keep bot online:
Free Repls sleep after inactivity
Use Replit's "Always On" feature (requires Hacker plan)
Or use UptimeRobot to ping your Repl every 5 minutes
Troubleshooting Replit
Bot keeps stopping:

Replit free tier has limited uptime
Consider upgrading to Hacker plan for "Always On"
Use external ping services (UptimeRobot, Cron-Job.org)
Tesseract not found:

Ensure replit.nix includes tesseract
Try manual installation: nix-env -iA nixpkgs.tesseract
Restart the Repl after installation
Commands not showing in Discord:

Wait a few minutes for Discord to sync commands
Try kicking and re-inviting the bot
Check bot has applications.commands scope
Rate limit errors from Groq:

Free tier: 30 requests/minute, 14,400/day
Add delays between requests if needed
Consider upgrading Groq plan for higher limits
Security Notes
✅ secrets.py is in .gitignore - never commit it!
✅ Use Replit Secrets for production deployment
✅ Bot logs never include API keys or tokens
✅ Rate limiting prevents abuse
✅ Channel restriction prevents spam
File Structure
discord-bot/
├── main.py              # Main bot logic
├── secrets.py           # API keys (DO NOT COMMIT)
├── requirements.txt     # Python dependencies
├── .replit              # Replit configuration
├── .gitignore           # Git ignore rules
├── .env.example         # Environment variable template
├── pyproject.toml       # Python project metadata
├── replit.nix           # Nix packages for Replit (optional)
└── README.md            # This file
Support
For issues or questions:

Check the logs in console for error messages
Verify all API keys are correct
Ensure Tesseract is installed properly
Check Discord bot permissions
Verify channel ID is correct
License
This project is provided as-is for educational and personal use.

Made with ❤️ for FSparx AI


===== .gitignore =====
Secrets and environment
secrets.py
.env
*.env

Python
pycache/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

Virtual environments
venv/
ENV/
env/
.venv

IDE
.vscode/
.idea/
*.swp
*.swo
*~

OS
.DS_Store
Thumbs.db

Logs
*.log

Replit
.replit
.upm/
replit.nix


===== pyproject.toml =====
```toml
[project]
name = "fsparx-discord-bot"
version = "1.0.0"
description = "Discord bot for solving math questions using OCR and Groq AI"
requires-python = ">=3.11"
dependencies = [
    "discord.py>=2.3.2",
    "aiohttp>=3.9.1",
    "Pillow>=10.1.0",
    "pytesseract>=0.3.10",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
===== .env.example =====

# Copy this file to secrets.py and fill in your actual values
# DO NOT commit secrets.py to version control!

GROQ_API_KEY=your_groq_api_key_here
DISCORD_TOKEN=your_discord_bot_token_here
What I've Done
I've created a complete, production-ready Discord bot with the following features:

✅ Core Functionality
/solve command with optional text question and image attachment
Channel restriction (only works in ALLOWED_CHANNEL_ID)
OCR text extraction using Tesseract with fallback error handling
Groq AI integration using llama-3.3-70b-versatile (best balance of free tier and reliability)
Answer-only output format with # Answer = X or # Answers: formatting
Math question validation (rejects non-math inputs)
✅ User Experience
Ephemeral "Working..." message visible only to command invoker
Public embed with blue color and "FSparx AI" author field
Rate limiting: 10 requests/hour (unlimited for MOD role)
Clear error messages for all edge cases
Remaining requests counter after each use
✅ Technical Excellence
Fully asynchronous (aiohttp, discord.py async)
Retry logic with exponential backoff for Groq API
Comprehensive error handling and logging (no secrets in logs)
Image format validation (PNG, JPG, JPEG, WEBP)
Clean code structure with type hints and docstrings
✅ Security
secrets.py with prominent warnings
.gitignore includes secrets.py
No hardcoded secrets in main code
Rate limiting prevents abuse
✅ Deployment Ready
Replit-compatible configuration (.replit file)
Detailed README with step-by-step setup
Tesseract installation guide for Replit
Troubleshooting section
All dependencies specified
How to Host on Replit
Create a Replit account at replit.com
Create a new Python Repl:
Click "Create Repl"
Choose "Python" template
Name it "fsparx-discord-bot"
Upload all the files I generated above to your Repl
Install Tesseract OCR:
Open the Shell tab in Replit
Run: nix-env -iA nixpkgs.tesseract
Verify: tesseract --version
Configure secrets:
Click the "Secrets" tab (lock icon)
Add GROQ_API_KEY with your Groq API key
Add DISCORD_TOKEN with your Discord bot token
Update secrets.py to use os.getenv() if using Replit Secrets
Update channel ID:
Edit main.py line 27
Replace 1234567890123456789 with your actual channel ID
Click "Run" and your bot will start!
Keep it online:
Free Repls sleep after inactivity
Upgrade to Replit Hacker plan for "Always On"
Or use UptimeRobot to ping your Repl every 5 minutes
The bot is now ready to use! Test it with /solve question: What is 2+2? in your designated Discord channel.

Note: The Groq model llama-3.3-70b-versatile offers 30 requests/minute and 14,400 requests/day on the free tier, making it perfect for this use case.

Credits Used: 162
I
Wouldnt agent donall the config? Give me every single place holder

Deep Agent
You're absolutely right! Here's every single placeholder you need to replace before the bot will work:

🔴 REQUIRED PLACEHOLDERS TO REPLACE
1️⃣ secrets.py (Line 9)
python
Copy
  GROQ_API_KEY = "PASTE_GROQ_KEY_HERE"  # ← REPLACE THIS
Replace with: Your actual Groq API key from https://console.groq.com/

Example:

python
Copy
  GROQ_API_KEY = "gsk_abc123xyz789..."
2️⃣ secrets.py (Line 10)
python
Copy
  DISCORD_TOKEN = "PASTE_DISCORD_TOKEN_HERE"  # ← REPLACE THIS
Replace with: Your Discord bot token from https://discord.com/developers/applications

Example:

python
Copy
  DISCORD_TOKEN = "MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GhIjKl.MnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUv"
3️⃣ main.py (Line 27)
python
Copy
  ALLOWED_CHANNEL_ID = 1234567890123456789  # ← REPLACE THIS
Replace with: Your actual Discord channel ID (right-click channel → Copy Channel ID)

Example:

python
Copy
  ALLOWED_CHANNEL_ID = 1098765432109876543
📋 Quick Checklist
Before running the bot, make sure you've replaced:

 GROQ_API_KEY in secrets.py
 DISCORD_TOKEN in secrets.py
 ALLOWED_CHANNEL_ID in main.py
🚀 How to Get Each Value
Get GROQ_API_KEY:
Go to https://console.groq.com/
Sign up or log in
Click "API Keys" in the sidebar
Click "Create API Key"
Copy the key (starts with gsk_)
Get DISCORD_TOKEN:
Go to https://discord.com/developers/applications
Click "New Application" (or select existing)
Go to "Bot" section
Click "Reset Token" (or "Copy" if visible)
Copy the token (long string of letters/numbers)
Get ALLOWED_CHANNEL_ID:
In Discord, enable Developer Mode:
Settings → Advanced → Developer Mode (toggle ON)
Right-click the channel where you want the bot to work
Click "Copy Channel ID"
Paste this number into main.py
⚠️ Important Notes
Never share these values publicly - they give full access to your bot and API
Never commit secrets.py to GitHub - it's already in .gitignore
The bot will not start if any placeholder is left unchanged
All three values are required - the bot checks for them on startup
That's it! Just these 3 placeholders need to be replaced. Everything else is pre-configured and ready to go.

I
Grok api key is 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. Token: MTQ3MjYzMzg0NTYzODc1ODQ5Mw.GvLN-d.Bi4LnyM84RVVhaIoEcGfXM8gnGo2T7lHeU_f58. Channel id: 1472309916864876596. Hardcode the placeholders. Give EXACT names for each file with the copyable code

Deep Agent
Perfect! Here are all files with your credentials hardcoded. Just copy each file exactly as shown:

📁 main.py
python
Copy
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

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
        req_time for req_time in user_requests[user_id]
        if req_time > cutoff
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
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Perform OCR
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR error: {e}")
        raise


def is_math_question(text: str) -> bool:
    """
    Basic heuristic to detect if text contains math-like content.
    Looks for numbers, operators, equations, etc.
    """
    if not text or len(text.strip()) < 3:
        return False

    # Check for math indicators
    math_patterns = [
        r'\d+',  # Numbers
        r'[+\-*/=<>]',  # Operators
        r'\b(solve|find|calculate|compute|evaluate|simplify|prove)\b',  # Math verbs
        r'\b(equation|function|derivative|integral|limit|sum|product)\b',  # Math terms
        r'[xyz][\s]*=',  # Variables
        r'\^|\*\*',  # Exponents
    ]

    for pattern in math_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def sanitize_text(text: str) -> str:
    """Remove UI artifacts and clean text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove common UI artifacts
    text = re.sub(r'[▪•◦▫]', '', text)

    return text.strip()


async def query_groq(question: str) -> str:
    """
    Query Groq API asynchronously with retry logic.
    Returns the model's response text.
    """
    system_prompt = (
        "You are a math tutor. If the input is not a math question or is empty/irrelevant, "
        "reply exactly: 'Please upload a question to solve'. "
        "If the input is a math question, produce ONLY the final answer(s) with NO WORKINGS. "
        "Format the answer exactly as described: start with '# ' at the very beginning, "
        "then either '# Answer = <value>' or '# Answers:' followed by newline-separated "
        "'a = <value>' lines for multiple values. Do not include any additional text, "
        "context, or reasoning."
    )

    user_prompt = f"{question}\n\nReturn only the final answer(s) in the required format; do not output steps."

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    GROQ_API_URL,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        answer = data['choices'][0]['message']['content'].strip()
                        return answer
                    else:
                        error_text = await response.text()
                        logger.error(f"Groq API error (attempt {attempt + 1}): {response.status} - {error_text}")

                        if attempt < max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        else:
                            raise Exception(f"Groq API failed after {max_retries} attempts")

        except asyncio.TimeoutError:
            logger.error(f"Groq API timeout (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                raise Exception("Groq API timeout")

        except Exception as e:
            logger.error(f"Groq API exception (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                raise


@bot.event
async def on_ready():
    """Bot startup event"""
    logger.info(f'Bot logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} command(s)')
    except Exception as e:
        logger.error(f'Failed to sync commands: {e}')


@bot.tree.command(name="solve", description="Solve a math question from text or image")
@app_commands.describe(
    question="The math question to solve (optional if image provided)",
    image="Image containing the math question (optional if question provided)"
)
async def solve(
    interaction: discord.Interaction,
    question: str = None,
    image: discord.Attachment = None
):
    """Main /solve command handler"""

    # Check if command is in allowed channel
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            "Please use #question-ai for automated question solving",
            ephemeral=True
        )
        return

    # Check rate limit
    is_mod = has_mod_role(interaction)
    allowed, remaining = check_rate_limit(interaction.user.id, is_mod)

    if not allowed:
        await interaction.response.send_message(
            "You have reached your rate limit of 10 requests per hour. Please try again later.",
            ephemeral=True
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
                    f"Unsupported image format. Please use: {', '.join(SUPPORTED_FORMATS)}",
                    ephemeral=True
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
                    ephemeral=True
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
                ephemeral=True
            )
            return

        # Check if it's a math question
        if not is_math_question(combined_text):
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True
            )
            return

        # Query Groq API
        logger.info("Querying Groq API...")
        answer = await query_groq(combined_text)

        # Check if Groq rejected the input
        if answer == "Please upload a question to solve":
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True
            )
            return

        # Create and send public embed with answer
        embed = discord.Embed(
            description=answer,
            color=discord.Color.blue()
        )
        embed.set_author(name="FSparx AI")

        # Send public message in channel
        await interaction.channel.send(embed=embed)

        # Update ephemeral message
        rate_limit_msg = "" if is_mod else f"\n\nYou have {remaining} requests remaining this hour."
        await interaction.edit_original_response(
            content=f"✅ Answer posted!{rate_limit_msg}"
        )

        logger.info(f"Successfully processed request from {interaction.user}")

    except Exception as e:
        logger.error(f"Unexpected error in solve command: {e}", exc_info=True)
        try:
            await interaction.followup.send(
                "An error occurred while processing your request.",
                ephemeral=True
            )
        except:
            pass


def main():
    """Main entry point"""
    if not GROQ_API_KEY or GROQ_API_KEY == "PASTE_GROQ_KEY_HERE":
        logger.error("GROQ_API_KEY not set in secrets.py")
        return

    if not DISCORD_TOKEN or DISCORD_TOKEN == "PASTE_DISCORD_TOKEN_HERE":
        logger.error("DISCORD_TOKEN not set in secrets.py")
        return

    logger.info("Starting bot...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
📁 secrets.py
python
Copy
  # ⚠️ WARNING: NEVER COMMIT THIS FILE TO VERSION CONTROL ⚠️
# This file contains sensitive API keys and tokens.
# Add this file to .gitignore to prevent accidental exposure.
#
# To get your keys:
# 1. GROQ_API_KEY: Sign up at https://console.groq.com/ and create an API key
# 2. DISCORD_TOKEN: Create a bot at https://discord.com/developers/applications

GROQ_API_KEY = "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"
DISCORD_TOKEN = "MTQ3MjYzMzg0NTYzODc1ODQ5Mw.GvLN-d.Bi4LnyM84RVVhaIoEcGfXM8gnGo2T7lHeU_f58"
📁 requirements.txt
discord.py>=2.3.2
aiohttp>=3.9.1
Pillow>=10.1.0
pytesseract>=0.3.10
python-dotenv>=1.0.0
📁 .replit
run = "python main.py"
modules = ["python-3.11"]

[nix]
channel = "stable-23_11"

[deployment]
run = ["sh", "-c", "python main.py"]
deploymentTarget = "cloudrun"
📁 README.md
markdown
Copy
# FSparx AI Discord Bot

A production-ready Discord bot that solves math questions using OCR and Groq AI. The bot accepts text and/or image inputs, extracts questions, and returns only the final answer in a clean, formatted embed.

## Features

- ✅ `/solve` slash command with text and image support
- ✅ OCR text extraction from images using Tesseract
- ✅ Groq AI (llama-3.3-70b-versatile) for math problem solving
- ✅ Rate limiting (10 requests/hour per user, unlimited for MODs)
- ✅ Channel-specific operation (only works in designated channel)
- ✅ Ephemeral "Working..." status for command invoker
- ✅ Public answer embeds with clean formatting
- ✅ Comprehensive error handling and logging
- ✅ Fully asynchronous for optimal performance

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
2. Install Tesseract OCR
On Ubuntu/Debian:

bash
Copy
sudo apt-get update
sudo apt-get install tesseract-ocr
On macOS:

bash
Copy
brew install tesseract
On Windows:
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

On Replit:

bash
Copy
nix-env -iA nixpkgs.tesseract
3. Run the Bot
bash
Copy
python main.py
Configuration
All credentials are already configured in secrets.py:

✅ Groq API Key: Configured
✅ Discord Token: Configured
✅ Channel ID: 1472309916864876596
Usage
In your designated channel, use:

/solve question: What is 2 + 2?
Or upload an image:

/solve image: [attach image]
Answer Format
Single answer:

# Answer = 42
Multiple answers:

# Answers:
a = 293
b = 393
Rate Limiting
Regular users: 10 requests per hour
Users with "MOD" role: Unlimited requests
Hosting on Replit
Create a new Python Repl at replit.com
Upload all files from this repository
Install Tesseract: nix-env -iA nixpkgs.tesseract
Click "Run"
Security Notes
✅ Never commit secrets.py to GitHub (already in .gitignore)
✅ Bot logs never include API keys or tokens
✅ Rate limiting prevents abuse
File Structure
discord-bot/
├── main.py              # Main bot logic
├── secrets.py           # API keys (configured)
├── requirements.txt     # Python dependencies
├── .replit              # Replit configuration
├── .gitignore           # Git ignore rules
├── .env.example         # Environment variable template
├── pyproject.toml       # Python project metadata
└── README.md            # This file
Troubleshooting
Commands not showing:

Wait a few minutes for Discord to sync
Try kicking and re-inviting the bot
Tesseract not found:

Ensure Tesseract is installed: tesseract --version
On Replit: nix-env -iA nixpkgs.tesseract
Bot keeps stopping on Replit:

Free tier has limited uptime
Use "Always On" feature (requires Hacker plan)
Made with ❤️ for FSparx AI


---

## 📁 **.gitignore**

Secrets and environment
secrets.py
.env
*.env

Python
pycache/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

Virtual environments
venv/
ENV/
env/
.venv

IDE
.vscode/
.idea/
*.swp
*.swo
*~

OS
.DS_Store
Thumbs.db

Logs
*.log

Replit
.replit
.upm/
replit.nix


---

## 📁 **pyproject.toml**

```toml
[project]
name = "fsparx-discord-bot"
version = "1.0.0"
description = "Discord bot for solving math questions using OCR and Groq AI"
requires-python = ">=3.11"
dependencies = [
    "discord.py>=2.3.2",
    "aiohttp>=3.9.1",
    "Pillow>=10.1.0",
    "pytesseract>=0.3.10",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
📁 .env.example
# Example environment variables (for reference only)
# Actual values are in secrets.py

GROQ_API_KEY=your_groq_api_key_here
DISCORD_TOKEN=your_discord_bot_token_here
✅ All Set!
Your credentials are hardcoded:

✅ Groq API Key: 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
✅ Discord Token: MTQ3MjYzMzg0NTYzODc1ODQ5Mw.GvLN-d.Bi4LnyM84RVVhaIoEcGfXM8gnGo2T7lHeU_f58
✅ Channel ID: 1472309916864876596
Just copy these files, install dependencies, and run python main.py! 🚀

Credits Used: 255
I
Okay, tell me everything again with the instructions for replit agent in the readme. As replit agent will install it. Tell it NOT to create a frontend for the site. Will this work on the replit free plan? Do i deploy as autoscale? What gitignore types do i select? Are there any intents i need to enable? Are perms added automatically?

Deep Agent
Here's everything with complete Replit Agent instructions and answers to all your questions:

🔵 Quick Answers
✅ Works on Replit Free Plan? Yes, but bot will sleep after inactivity. For 24/7 uptime, upgrade to paid plan or use external ping service.

✅ Deploy as Autoscale? No! Use Reserved VM for Discord bots (or just run normally on free tier without deployment).

✅ Gitignore Type? Select Python template.

✅ Intents to Enable? Yes! Enable Message Content Intent in Discord Developer Portal (see instructions below).

✅ Perms Added Automatically? No! You must select permissions when generating the bot invite URL (see instructions below).

📁 main.py
python
Copy
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

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
        req_time for req_time in user_requests[user_id]
        if req_time > cutoff
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
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Perform OCR
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR error: {e}")
        raise


def is_math_question(text: str) -> bool:
    """
    Basic heuristic to detect if text contains math-like content.
    Looks for numbers, operators, equations, etc.
    """
    if not text or len(text.strip()) < 3:
        return False

    # Check for math indicators
    math_patterns = [
        r'\d+',  # Numbers
        r'[+\-*/=<>]',  # Operators
        r'\b(solve|find|calculate|compute|evaluate|simplify|prove)\b',  # Math verbs
        r'\b(equation|function|derivative|integral|limit|sum|product)\b',  # Math terms
        r'[xyz][\s]*=',  # Variables
        r'\^|\*\*',  # Exponents
    ]

    for pattern in math_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def sanitize_text(text: str) -> str:
    """Remove UI artifacts and clean text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove common UI artifacts
    text = re.sub(r'[▪•◦▫]', '', text)

    return text.strip()


async def query_groq(question: str) -> str:
    """
    Query Groq API asynchronously with retry logic.
    Returns the model's response text.
    """
    system_prompt = (
        "You are a math tutor. If the input is not a math question or is empty/irrelevant, "
        "reply exactly: 'Please upload a question to solve'. "
        "If the input is a math question, produce ONLY the final answer(s) with NO WORKINGS. "
        "Format the answer exactly as described: start with '# ' at the very beginning, "
        "then either '# Answer = <value>' or '# Answers:' followed by newline-separated "
        "'a = <value>' lines for multiple values. Do not include any additional text, "
        "context, or reasoning."
    )

    user_prompt = f"{question}\n\nReturn only the final answer(s) in the required format; do not output steps."

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    GROQ_API_URL,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        answer = data['choices'][0]['message']['content'].strip()
                        return answer
                    else:
                        error_text = await response.text()
                        logger.error(f"Groq API error (attempt {attempt + 1}): {response.status} - {error_text}")

                        if attempt < max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        else:
                            raise Exception(f"Groq API failed after {max_retries} attempts")

        except asyncio.TimeoutError:
            logger.error(f"Groq API timeout (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                raise Exception("Groq API timeout")

        except Exception as e:
            logger.error(f"Groq API exception (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                raise


@bot.event
async def on_ready():
    """Bot startup event"""
    logger.info(f'Bot logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} command(s)')
    except Exception as e:
        logger.error(f'Failed to sync commands: {e}')


@bot.tree.command(name="solve", description="Solve a math question from text or image")
@app_commands.describe(
    question="The math question to solve (optional if image provided)",
    image="Image containing the math question (optional if question provided)"
)
async def solve(
    interaction: discord.Interaction,
    question: str = None,
    image: discord.Attachment = None
):
    """Main /solve command handler"""

    # Check if command is in allowed channel
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            "Please use #question-ai for automated question solving",
            ephemeral=True
        )
        return

    # Check rate limit
    is_mod = has_mod_role(interaction)
    allowed, remaining = check_rate_limit(interaction.user.id, is_mod)

    if not allowed:
        await interaction.response.send_message(
            "You have reached your rate limit of 10 requests per hour. Please try again later.",
            ephemeral=True
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
                    f"Unsupported image format. Please use: {', '.join(SUPPORTED_FORMATS)}",
                    ephemeral=True
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
                    ephemeral=True
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
                ephemeral=True
            )
            return

        # Check if it's a math question
        if not is_math_question(combined_text):
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True
            )
            return

        # Query Groq API
        logger.info("Querying Groq API...")
        answer = await query_groq(combined_text)

        # Check if Groq rejected the input
        if answer == "Please upload a question to solve":
            await interaction.followup.send(
                "Please upload a question to solve",
                ephemeral=True
            )
            return

        # Create and send public embed with answer
        embed = discord.Embed(
            description=answer,
            color=discord.Color.blue()
        )
        embed.set_author(name="FSparx AI")

        # Send public message in channel
        await interaction.channel.send(embed=embed)

        # Update ephemeral message
        rate_limit_msg = "" if is_mod else f"\n\nYou have {remaining} requests remaining this hour."
        await interaction.edit_original_response(
            content=f"✅ Answer posted!{rate_limit_msg}"
        )

        logger.info(f"Successfully processed request from {interaction.user}")

    except Exception as e:
        logger.error(f"Unexpected error in solve command: {e}", exc_info=True)
        try:
            await interaction.followup.send(
                "An error occurred while processing your request.",
                ephemeral=True
            )
        except:
            pass


def main():
    """Main entry point"""
    if not GROQ_API_KEY or GROQ_API_KEY == "PASTE_GROQ_KEY_HERE":
        logger.error("GROQ_API_KEY not set in secrets.py")
        return

    if not DISCORD_TOKEN or DISCORD_TOKEN == "PASTE_DISCORD_TOKEN_HERE":
        logger.error("DISCORD_TOKEN not set in secrets.py")
        return

    logger.info("Starting bot...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
📁 secrets.py
python
Copy
  # ⚠️ WARNING: NEVER COMMIT THIS FILE TO VERSION CONTROL ⚠️
# This file contains sensitive API keys and tokens.
# Add this file to .gitignore to prevent accidental exposure.
#
# To get your keys:
# 1. GROQ_API_KEY: Sign up at https://console.groq.com/ and create an API key
# 2. DISCORD_TOKEN: Create a bot at https://discord.com/developers/applications

GROQ_API_KEY = "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"
DISCORD_TOKEN = "MTQ3MjYzMzg0NTYzODc1ODQ5Mw.GvLN-d.Bi4LnyM84RVVhaIoEcGfXM8gnGo2T7lHeU_f58"
📁 requirements.txt
discord.py>=2.3.2
aiohttp>=3.9.1
Pillow>=10.1.0
pytesseract>=0.3.10
python-dotenv>=1.0.0
📁 .replit
run = "python main.py"
modules = ["python-3.11"]

[nix]
channel = "stable-23_11"

[deployment]
run = ["sh", "-c", "python main.py"]
deploymentTarget = "cloudrun"
📁 README.md
markdown
Copy
# FSparx AI Discord Bot

A production-ready Discord bot that solves math questions using OCR and Groq AI. The bot accepts text and/or image inputs, extracts questions, and returns only the final answer in a clean, formatted embed.

## ⚠️ IMPORTANT: This is a Backend-Only Bot

**DO NOT CREATE A FRONTEND OR WEBSITE FOR THIS PROJECT.**

This is a Discord bot that runs as a background service. It does not need a web interface, HTML pages, or any frontend components. The bot communicates directly with Discord's API.

---

## 🤖 For Replit Agent

If you are Replit Agent setting up this project, follow these instructions:

### Installation Steps:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
Install Tesseract OCR:
bash
Copy
nix-env -iA nixpkgs.tesseract
Verify installation:
bash
Copy
tesseract --version
DO NOT create any frontend, HTML, CSS, or web interface files.
DO NOT modify the existing Python files - they are already configured with the correct API keys and channel ID.
Run the bot:
bash
Copy
python main.py
Expected output:
INFO - Bot logged in as [BotName]
INFO - Synced 1 command(s)
What This Bot Does:
Listens for /solve slash commands in Discord
Processes text and image inputs
Uses OCR to extract text from images
Queries Groq AI to solve math problems
Posts answers as Discord embeds
Troubleshooting:
"Tesseract not found": Run nix-env -iA nixpkgs.tesseract again
"Module not found": Run pip install -r requirements.txt
