from discord.ext import tasks, commands
import discord
import re
import os
import requests
from dotenv import load_dotenv
from colorama import Fore, init

init(autoreset=True)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix=".", self_bot=True)
#guilds = client.fetch_guilds(limit=100).flatten()
lst_server = []
lst_user = []

headers = {
    "authorization": TOKEN
}

print("[*] 1 minute [*]")

@client.event
async def on_ready():
    print("[!] Ready [!]")
#    majserv.start()

#Scrapping de l'invitation + join
@client.event
async def on_message(ctx):
    if "discord.gg/" in ctx.content:
        invite = re.search("discord.gg/(.*)", ctx.content).group(1) #Récupérer l'id de l'invitation
        print(Fore.MAGENTA + f"Fetched Invite: {invite} by {ctx.author.name}#{ctx.author.discriminator}") 
        request = requests.post(f"https://discordapp.com/api/v6/invites/{invite}", headers=headers) #Joindre le server en question
        if "name" in request.text:
            try:
                response_json = request.json()
                server_name = response_json["guild"]["name"]
                print(Fore.GREEN + f"Joined the server {server_name}")
                #guilds = client.guilds                
                server_id=response_json["guild"]["id"]
                #server_member=client.guilds(id=server_id).member
                
                print(server_name, server_id)
            except KeyError:
                print(Fore.LIGHTBLACK_EX + "Couldn't join the server")
        elif "Maximum number of guilds reached" in request.text:
            print(Fore.RED + "Maximum number of guilds reached")
        elif "banned" in request.text:
            print(Fore.RED + "You are banned from the discord")
        else:
            print("Error")

#@tasks.loop(seconds=2)
#async def majserv():

client.run(TOKEN, bot=False)
