# FSparx AI Discord Bot

A Discord bot that solves math questions using OCR and Groq AI. The bot accepts text and/or image inputs and returns only the final answer in a embed.

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
"Tesseract not found": Run nix-env -iA nixpkgs.tesseract again
"Module not found": Run pip install -r requirements.txt
