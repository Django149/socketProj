import discord
import json
from discord.ext import commands
import asyncio
from script import *

token = 'OTg3MDg3NzIxNzI4MjAwNzc0.Gx8CUe.gr3UVsKg_7JswJ8z8szyTPaj1yMCxrD_Sg2pNs'

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("Bot Running!")
    await bot.change_presence(activity=discord.Game(name="lil's bot"))


@bot.command()
async def Torim(ctx):
    locations = get_locations()
    all_cities = []
    for location in locations:
        all_cities.append(location['LocationName'])
    embedVar = discord.Embed(title="**___כל הלשכות___**", color=0x00ff00)
    for city in all_cities:
        embedVar.add_field(name=city[5:], value="ㅤ", inline=True)
    await ctx.send(embed=embedVar)
    embedVar = discord.Embed(title="", description="כדי לראות את התורים הזמינים בלשכה שתבחר, כתוב **!Times** ולאחר מכן את שם הלשכה בה תרצה להציג את התורים הזמינים",color=0x00ff00)
    await ctx.send(embed=embedVar)
    #await ctx.channel.send()


@bot.command()
async def Times(ctx, *message):
    message = ' '.join(message)
    print(message)
    all_times = ""
    locations = get_locations()
    for location in locations:
        if message == location['LocationName'][5:]:
            lst = get_dates(location['ServiceId'])
            all_times = '\n'.join(['  |  '.join(lst[i: i+3]) for i in range(0, len(lst), 3)])
    await ctx.channel.send(all_times)



bot.run(token)