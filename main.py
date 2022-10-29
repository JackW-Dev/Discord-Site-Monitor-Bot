import functools
from urllib.request import urlopen, Request
from discord.ext import commands
import discord
import hashlib
import time

discord_token = INSERT_DISCORD_TOKEN_HERE
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
web_url = ""
run_thread = True


@bot.event
async def on_ready():
    print(f'{bot.user} successfully logged in!')


@bot.command()
async def set_site(ctx, url):
    global web_url
    web_url = url
    await ctx.send(f'Tracked URL updated to: {url}')
    return


@bot.command()
async def get_site(ctx):
    global web_url
    await ctx.send(f'Tracked URL is currently: {web_url}')
    return


@bot.command()
async def start_monitoring(ctx):
    global web_url
    global run_thread

    run_thread = True
    role = discord.utils.get(ctx.guild.roles, name="BotUpdates")
    request = Request(web_url)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                                     'like Gecko) Chrome/103.0.0.0 Safari/537.36')
    url_response = urlopen(request).read()
    current_hash = hashlib.sha224(url_response).hexdigest()

    await ctx.send(f'Script started')

    while run_thread:
        try:
            url_response = urlopen(request).read()
            current_hash = hashlib.sha224(url_response).hexdigest()

            await run_blocking(blocking_func)
            # await ctx.send(f'Waited 30 seconds')
            # print(f'Waited 30 seconds')

            url_response = urlopen(request).read()
            new_hash = hashlib.sha224(url_response).hexdigest()

            if new_hash != current_hash:
                await ctx.send(f'{role.mention} Site has been updated')

                run_thread = False

        except Exception as e:
            await ctx.send(f'{role.mention} Something went wrong  + {e}')

    await ctx.send(f'Monitoring stopped')

    return


@bot.command()
async def stop_monitoring(ctx):
    global run_thread
    run_thread = False
    await ctx.send(f'Monitoring stopped')
    return


def blocking_func():
    time.sleep(30)
    return


async def run_blocking(blocker_func):
    func = functools.partial(blocker_func)
    return await bot.loop.run_in_executor(None, func)

bot.run(discord_token)
