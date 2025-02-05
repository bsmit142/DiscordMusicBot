import os
import logging
import discord
import json
from bot.config import BASE_POINTS, CLAIM_POINTS, CLAIM_COOLDOWN_PERIOD, LOAN_INTEREST_RATE
from discord.ext import commands
from dotenv import load_dotenv
from bot.utils.json_handler import load_json, save_json
from bot.commands import betting, music, user_management, fun, roll

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setup logging
logging.basicConfig(level=logging.INFO)

# Bot setup
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Load data files
POINTS_FILE = '/opt/music_bot/user_points.json'
BET_HISTORY_FILE = '/opt/music_bot/bet_history.json'
LOANS_FILE = '/opt/music_bot/loans.json'

# Default data to be used if files are missing
default_data = {}

# Function to ensure files exist and create them if missing
def ensure_file_exists(file_path, default_content):
    if not os.path.exists(file_path):
        logging.info(f"{file_path} not found. Creating new file.")
        with open(file_path, 'w') as f:
            json.dump(default_content, f)

user_points = load_json(POINTS_FILE)
bet_history = load_json(BET_HISTORY_FILE)
loans = load_json(LOANS_FILE)

# Register commands
betting.setup(bot, BASE_POINTS, CLAIM_POINTS, CLAIM_COOLDOWN_PERIOD, LOAN_INTEREST_RATE, user_points, bet_history, loans, POINTS_FILE, BET_HISTORY_FILE, LOANS_FILE)
music.setup(bot)
user_management.setup(bot, user_points, POINTS_FILE, LOANS_FILE)
fun.setup(bot)
roll.setup(bot, BASE_POINTS, user_points, POINTS_FILE)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is now running!')

@bot.event
async def on_disconnect():
    save_json(POINTS_FILE, user_points)
    save_json(BET_HISTORY_FILE, bet_history)
    save_json(LOANS_FILE, loans)

bot.run(TOKEN)
