import settings
import discord
import requests
from discord.ext import commands
import datetime, asyncio

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
        await schedule_daily_message()

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

    async def post_daily_problem(channel):
        problem_data = fetch_daily_problem()
        if problem_data:
            problem_title = problem_data['questionTitle']
            problem_link = problem_data['questionLink']
            message = f"# Today's LeetCode Daily Problem:\n\n**{problem_title}**\n{problem_link}\n\nGood Luck! (Don't post your solutions without a spoiler!)"
        else:
            message = "# Error procuring today's problem\nTry again later :("
        await channel.send(message)


    async def schedule_daily_message():
        while True:
            now = datetime.datetime.now()
            then = now.replace(hour=0, minute=0, second=0, microsecond=0)
            if now >= then:
                then += datetime.timedelta(days=1)
            wait_time = (then - now).total_seconds()
            logger.info(f"Waiting for {wait_time} seconds until next post.")
            await asyncio.sleep(wait_time)
            channel = bot.get_channel(settings.CHANNEL_ID)
            if channel:
                await post_daily_problem(channel)
            else:
                logger.error("Channel not found. Ensure the CHANNEL_ID is correct.")




    bot.run(settings.TOKEN, root_logger=True)


if __name__ == "__main__":
    run()
