from discord.ext import commands
from whatsnext import Whatsnext
from ruamel.yaml import YAML
from datetime import datetime, timedelta
import math

bot = commands.Bot(command_prefix='$')

yaml = YAML()
with open('mvla2020-21.yaml') as f:
    schedule_base = yaml.load(f)
inst = Whatsnext(schedule_base)

def view(now):
    period = inst.next(now)
    last_class = inst.prev(now)

    start = period['start']
    end = period['end']

    def till(a, b):
        return b - a
    length = till(start, end)
    # only make sense before class
    between = till(last_class['end'], start)
    until = till(now, start)
    # only make sense during class
    left = till(now, end)
    elapsed = till(start, now)

    try:
        percent = until / between
    except ZeroDivisionError:
        percent = 0
    diff = until

    if start < now < end:
        percent = elapsed / length
        diff = left

    return {
            "last": last_class,
            "next": period,
            "countdown": timedelta(seconds=math.ceil(diff.total_seconds())),
            "percent": percent,
            "percent_formatted": f"{percent*100:0.2f}%",
    }

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!");

@bot.command()
async def period(ctx):
    period = view(datetime.now())
    await ctx.send("{next[id]} {countdown} {percent_formatted}".format(**period));

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run('PUT BOT KEY HERE')
