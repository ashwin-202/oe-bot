import os, asyncio
import discord
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"].strip()
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"].strip()

ai = genai.Client(api_key=GEMINI_API_KEY)      # the brain
MODEL = "gemini-3.6-flash"

SYSTEM = (
    "You are oe-bot, Ash's thinking partner inside ASHWORLD — a personal operating "
    "system of the Opportunity Engine (OE), LARPAI (a living radar for the AI frontier), "
    "and Opportunistic Polymathy (lifetime breadth, seasonal depth). Help Ash notice, "
    "connect, learn, build, prove, and compound opportunities across many fields "
    "(cyber, AI, systems, finance, biomed...). Be concise, concrete, and honest; push "
    "back when useful; turn ideas into a next physical action; never invent facts — say "
    "when unsure."
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:          # ignore itself
        return
    async with message.channel.typing():       # show "typing..." while it thinks
        try:
            resp = await asyncio.to_thread(     # run the blocking AI call off the main loop
                lambda: ai.models.generate_content(
                    model=MODEL,
                    contents=message.content,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM),
                )
            )
            reply = resp.text or "(no reply)"
        except Exception as e:
            reply = f"⚠️ brain error: {e}"
    await message.channel.send(reply[:1990])    # Discord caps messages at 2000 chars

client.run(DISCORD_TOKEN)