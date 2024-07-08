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
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user}")

    @bot.command()
    async def daily(ctx):
        """Posts Daily Question"""
        problem_data = fetch_daily_problem()

        if problem_data:
            problem_title = problem_data['questionTitle']
            problem_link = problem_data['questionLink']
            message = f"# Today's LeetCode Daily Problem:\n\n**{problem_title}**\n{problem_link}\n\nGood Luck! (Don't post your solutions without a spoiler!)"

        else:
            message = "# Error procuring todays problem\nTry again later :("

        await ctx.send(message)


    bot.run(settings.TOKEN, root_logger=True)


if __name__ == "__main__":
    run()
