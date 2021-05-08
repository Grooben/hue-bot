import discord
import os
import hue

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

token = os.getenv('D_TOKEN')

huebot = commands.Bot(command_prefix='!')

@huebot.event
async def on_ready():
    print(f'{huebot.user} has connected to Discord')

@huebot.command(name="off")
async def off(ctx, arg):
    arg = int(arg, base=10)
    hue.turnOffLight(arg)
    await status(ctx, arg)

@huebot.command(name="on")
async def on(ctx, arg):
    arg = int(arg, base=10)
    hue.turnOnLight(arg)
    await status(ctx, arg)

@huebot.command(name="status")
async def status(ctx, arg = "all"):
    lights = hue.getLights()
    embed = discord.Embed(title="Lights Status", description="The status of the currently connected lights", color=0x08d8e7) 
    embed.set_author(name="H.U.E")
    if arg == "all":
        count = 0
        while (count <= len(lights)):
            try:
                tmpCnt = count + 1
                if tmpCnt >= (len(lights) + 1): break # break out of the loop if we stray out of bounds
                statusStr = hue.getLightStatusSimp(tmpCnt)
                embed.add_field(name = lights[str(tmpCnt)]["name"], value = statusStr)
            except Exception as e:
                print("Something fucking dreadful has happened: {0}".format(e))
                break
            count =count + 1 
        await ctx.send(embed=embed)
    else:
        try:
            print("Status request on light {0}".format(str(arg)))
            statusStr = hue.getLightStatusDetailed(arg)
            embed.add_field(name = lights[str(arg)]["name"], value = statusStr)
        except Exception as e:
            print(e)
            embed = discord.Embed(title="404, light not found", description="H.U.E couldn't find that light, it either doesn't exist or isn't very happy", color=0x08d8e7)
            embed.set_author(name="H.U.E")
        await ctx.send(embed=embed)

print("H.U.E. is now connecting to Discord...")   
huebot.run(token)

