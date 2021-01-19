# README

This discord `worm` join every server it found. To do that, the worm search in the new messages for invitations and also collect these data :
  
- Server name
- ID Code of the server
- Name and ID of the people and bots in the server
Next to come :
- Every messages associated to users
- Tracking connection status

## General overview

This program has 3 parts : 
- The worm (deterre.py)
- The server (Django part)
- The analyser (next to come)

The worm : 
- Collect data on discor and make POST requests to the django API to store what it found in a DB

The server : 
- Receive the API calls and perform modifications in DB
- An admin interface on django is enable to modify / access the data 

The analyser (not live yet):
- Collect data from the server
- Anaylse and transform the data
- Create graphical views

## How to ...?

**Launch the server**
``` bash
cd siteweb/
python3 manage.py runserver
```

**Create admin user:**
``` bash
cd siteweb/
python3 manage.py createsuperuser
```  

**Make migration (to update the data model):**
``` bash
python3 manage.py makemigrations
python3 manage.py migrate
```

**Launch the worm:**
- You need a discord account, get the `DISCORD_TOKEN`that allows you to use the API
- Start the server
- Then: 
``` bash
# Setup env
export DISCORD_TOKEN=<your_token>
# or edit ver/.env

python3 ver/deterre-v2.py
```
- FInally lanch a first invitation link on your root server where the worm is and... let's go !

# Contributeurs 

- VictorLuc4
- Dadoo-A