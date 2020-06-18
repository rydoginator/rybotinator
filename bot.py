import json
import discord 
import os
import discord
from dotenv import load_dotenv

load_dotenv()

# load the token
TOKEN = os.getenv('DISCORD_TOKEN')

NOURL = "https://upload.wikimedia.org/wikipedia/commons/0/0a/No-image-available.png"
# start the client
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if ';get' in message.content:
        needle = ''
        items = []
        if message.content[5] == '"' and message.content[-1] == '"':
            needle = message.content[6:-1].lower()
            items = quoteFindItem(needle)
        # comparing strings in lowercase always works, right?
        else:
            needle = message.content[5:].lower()
            items = findItem(needle)
        if len(items) > 10:
            await message.channel.send("Too many results! Please redefine your search.\nTry quote searching for definite results!")
        elif len(items) == 0:
            await message.channel.send("No results!")
        else:
            for item in items:
                embed = ''
                if "color" in item:
                    if "DiyRecipe" in item:
                        embed=discord.Embed(title=item["color"] + " " + item["name"], description="id: " + item["id"][1]+"\ndiy: " + item["DiyRecipe"][1], color=0x00ff00)
                        embed.set_thumbnail(url = findPicture(item))
                    else:
                        embed=discord.Embed(title=item["color"] + " " + item["name"], description=item["id"][1], color=0x00ff00)
                        embed.set_thumbnail(url = findPicture(item))
                else:
                    if "DiyRecipe" in item:
                        embed=discord.Embed(title=item["name"], description="id: " + item["id"][1]+"\ndiy: " + item["DiyRecipe"][1], color=0x00ff00)
                        embed.set_thumbnail(url = findPicture(item))
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
            if needle in item["name"].lower():
                res.append(item)
    return res

def quoteFindItem(needle):
    with open("items_USen.json") as f:
        haystack = json.load(f)
    res = []
    for key, value in haystack.items():
        for item in value:
            if needle == item["name"].lower():
                res.append(item)
                return res 

def findPicture(needle):
    with open("items.json", encoding="utf8") as f:
        haystack = json.load(f)
    for hay in haystack:
        if needle["name"].lower() == hay["name"].lower():
            for barn in hay["variants"]:
                if "image" in barn:
                    return barn["image"]
                elif "storageImage" in barn:
                    if barn["storageImage"] is None:
                        if "inventoryImage" in barn:
                            if barn["inventoryImage"] is None:
                                return NOURL
                            else:
                                return barn["inventoryImage"]
                    else:
                        return barn["storageImage"]
                elif "inventoryImage" in barn:
                    if barn["inventoryImage"] is None:
                        return NOURL
                    else:
                        return barn["inventoryImage"]
                else:
                    return NOURL
    return NOURL



client.run(TOKEN)