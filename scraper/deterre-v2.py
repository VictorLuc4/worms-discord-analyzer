from discord.ext import tasks, commands
import discord
import re
import os
import requests
from dotenv import load_dotenv
from colorama import Fore, init
from dotenv import load_dotenv
import base64

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
    #majserver.start()

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
                server_id=response_json["guild"]["id"]

                data_server = {'name':server_name, 'code':server_id}
                api = requests.post(f"http://127.0.0.1:8000/worm/server/", data=data_server)

                data_members = {'members':[{}, {}]} # This for security reason, I do not trust them
                
                for member in client.get_all_members():
                    print("ID:",member.id," NAME:",member.name,"GUILD:", member.guild, "ACTIVITIES:",member.activities, "STATUS:",member.status,"WEB:",member.web_status,"PERM:",member.guild_permissions)
                    tmp = {'id':str(member.id), 'username':member.name, 'server':member.guild.name.replace("'", "\\'")}
                    data_members['members'].append(tmp)
                
                message = str(data_members)
                message_bytes = message.encode('utf-8')
                base64_bytes = base64.b64encode(message_bytes)
                base64_message = base64_bytes.decode('utf-8')
                encoded_message = {'encoded':base64_message}
                api = requests.post(f"http://127.0.0.1:8000/worm/person/", data=encoded_message)

            except KeyError:
                print(Fore.LIGHTBLACK_EX + "Couldn't join the server")
        elif "Maximum number of guilds reached" in request.text:
            print(Fore.RED + "Maximum number of guilds reached")
        elif "banned" in request.text:
            print(Fore.RED + "You are banned from the discord")
        else:
            print("Error")

client.run(TOKEN, bot=False)
