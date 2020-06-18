import json
import discord 
import os
import discord
from dotenv import load_dotenv

load_dotenv()

# load the token
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if ';get' in message.content:
        needle = message.content[5:]
        # ok, this is shitty, ill fix
        items = findItem(needle)
        if len(items) > 10:
            await message.channel.send("Too many results! Please redefine your search.")
        elif len(items) == 0:
            await message.channel.send("No results!")
        else:
            for item in items:
                if "color" in item:
                    embed=discord.Embed(title=item["color"] + " " + item["name"], description=item["id"][1], color=0x00ff00)
                    embed.set_thumbnail(url = findPicture(item))
                    await message.channel.send(embed=embed)
                else:
                    embed=discord.Embed(title=item["name"], description=item["id"][1], color=0x00ff00)
                    embed.set_thumbnail(url = findPicture(item))
                    await message.channel.send(embed=embed)

def findItem(needle):
    with open("items_USen.json") as f:
        haystack = json.load(f)
    res = []
    for key, value in haystack.items():
        for item in value:
            if needle in item["name"]:
                res.append(item)
    return res

def findPicture(needle):
    with open("items.json", encoding="utf8") as f:
        haystack = json.load(f)
    for hay in haystack:
        if needle["name"] == hay["name"]:
            for hays in hay["variants"]:
                if "image" in hays:
                    return hays["image"]
                else:
                	return "https://acnhcdn.com/latest/noImage.png"

def printResults(results):
    if len(results) > 20:
        return 'Too many results! Please redefine your search.'
    elif len(results) == 0:
        return 'No results!'
    else:
        res = "I've found:\n```c\n"
        for result in results:
            if "color" in result:
                res += "\nName: " + result["color"] + " " + result["name"] + " " + "\nid:" + result["id"][1]
            else:
                res += "\nName: " + result["name"] + "\nid: " + result["id"][1]
        return res + "\n```" 

client.run(TOKEN)