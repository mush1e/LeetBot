import settings
import discord
import requests
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def fetch_daily_problem():
    url = 'https://alfa-leetcode-api.onrender.com//daily'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return None

def run():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user}")

    bot.run(settings.TOKEN, root_logger=True)


if __name__ == "__main__":
    run()
