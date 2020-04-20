#
# In this program we are going to get the data from the server
# Then transform it to make it interesting
# Then template it in VueJS files to render graphics and tabs
#

import requests

fulltext = ""
all_people = []

def get_fulltext_from_template():
    lines = []
    fd = open("./analyser.js.template")
    for line in fd:
        lines.append(line)
    fulltext = fulltext.join(lines)

# Cette fonction remplace {to_replace} par des donnees str ou nombre comme ["Paris", "New-York", "Tokyo"] ou [1, 2, 3, 4]
def template_this(to_replace, table, is_str = True):
    labels = "["
    for item in table:
        if is_str:
            labels = labels + '"' + str(item) + '"'
        else:
            labels = labels + item
        labels = labels + ", "
        i += 1 
        if i > 20:
            break
    labels = labels[0:len(labels) - 2] + "]"
    fulltext = fulltext.replace(to_replace, labels)

def get_servers():
    req = requests.get("http://127.0.0.1:8000/worm/servers/")
    data = req.json()
    for serv in data:
        print(serv)

def get_users():
    req = requests.get("http://127.0.0.1:8000/worm/persons/")
    data = req.json()
    for user in data:
        print(user)


print('Hello Servers')
get_servers()
print('Hello Users')
get_users()