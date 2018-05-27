v = "0.1.0"
#--buildpack heroku/python

# -*- coding: utf-8 -*-
"""
Created on Thu May 24 23:33:38 2018

@author: Student
"""
import datetime

def replace(file,searchExp,replaceExp):
    import fileinput
    import sys
    for line in fileinput.input(file, inplace=1):
        if line.startswith(searchExp):
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def today():
    today = datetime.date.today()
    r = str(today).split("-")
    return r

def downtime(quests, startdate = "0-0-0", spent = 0):
    x = str(startdate).split("-")
    y = today()
    w = []
    for z in range (0,3):
        w.append(int(int(y[z])-int(x[z])))
    try:
        s = int(spent)
        q = int(quests)
    except:
        return "Syntax error, spent days should be an integer."
    dt = w[0]*365 + w[1]*30 + w[2] + q - s
    return dt

def reset(usr, cname):
    infile = "dtbot.txt"
    done = 0
    if usr == "":
        return "Invalid user"
    print("user " + str(usr) + " with character " + str(cname) + " has reset their dt days to 0.")    
    ls = str(usr) + "\t" + str(cname)
    l0 = str(ls) + "\t" + str(datetime.date.today())+ "\t" + "0" + "\t0" + "\t\n"
    with open(infile, "r") as f:
        d = f.readlines()
        tick = 0
        flag = 0
        f.seek(0)
        for i in d:
            if i.startswith(str(usr)):
                tick +=1
            if i.startswith(ls):
                flag = 1
        if tick >= 2 and flag == 0:
            x = "You have " + str(tick) + " Characters on record already. If one needs deleting, use the delete command"
            return x
    with open(infile,"r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if ls in i:
                f.write(l0)
                done = 1
            else:
                f.write(i)
        f.truncate()
    if done == 1:
        return "Character dt days reset successfully"
    f.close()
    if done == 0:
        print("User character combination not found. New entry added to " + str(infile))
        f = open(infile, "a")
        f.seek(2)
        f.write(l0)
        f.close()
        done = 1
        return "User character combination not found so added."
    f.close()

def quest(usr, cname):
    done = 0
    ls = str(usr) + "\t" + str(cname)
    infile = "dtbot.txt"
    la = ""
    if usr == "":
        return "Invalid user input"
    with open(infile, "r+") as f:
        d = f.readlines()
        f.seek(0)
        n = 0
        for i in d:
            if ls in i:
                r = d[n].split("\t")
                rt = int(r[3]) + 1
                la = str(ls) + "\t" + r[2] + "\t" + str(rt) + "\t"+ str(r[4]) + "\t\n"
                f.write(la)
                done = 1
            else:
                f.write(i)
            n += 1
        f.truncate()
    print("Usr: " + str(usr) + " added 1 quest to " + str(cname))
    if done == 0:
        return "User, character match not found, make sure you've got the name right."
    if done == 1:
        rv = "Quest addition successful, this character has been on " + str(rt) + " quest"
        if rt != 1:
            rv += "s"
        return rv
    
def spend(usr, cname, spent = 1):
    av = read(usr, cname)
    if int(spent) > int(av):
        x = "You only have " + str(av) + " dt avaliable."
        if int(av) == 0:
            x = "you have no downtime, go on some quests or just wait a bit"
        return x
    print(str(usr) + " just spent " + str(spent) + " dt")
    done = 0
    ls = str(usr) + "\t" + str(cname)
    infile = "dtbot.txt"
    try:
        rs = int(spent)
    except:
        return "Spent not an integer."
    if rs < 1:
        return "Input error, add less than 1"
    with open(infile, "r+") as f:
        d = f.readlines()
        n = 0
        f.seek(0)
        for i in d:
            if ls in i:
                r = d[n].split("\t")
                rt = int(r[4]) + rs
                ra = str(r[0]) + "\t" + str(r[1]) + "\t" + str(r[2]) + "\t" + str(r[3]) + "\t" + str(rt) + "\t\n"                
                f.write(ra)
                done = 1
            else:
                f.write(i)
            n += 1
        f.truncate()
    if done == 1:
        y = "The downtime is recorded, you now have " + str(read(usr,cname)) + " dt left"
    elif done == 0:
        y = "Name combination not found."
    return y
        
        
def read(usr, cname):
    print(str(usr)+" checked " + str(cname) + "'s dt")
    infile = "dtbot.txt"
    d = ""
    n = 0
    i = ""
    r = []
    q = ""
    sd = ""
    spent = 0
    ls = str(usr) + "\t" + str(cname)
    with open(infile, "r") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i.startswith(ls):
                r = d[n].split("\t")
                q = int(r[3])
                spent = int(r[4])
                sd = r[2]
                x = downtime(q,sd,spent)
            n += 1
        try:
            if x < 0:
                s = str(x)  + " (Apparently you have a negative number of days, resetting might help)" 
                return s
            else:
                s = str(x)
                return x
        except:
            return "Not found."

def delete(usr, cname):
    infile = "dtbot.txt"
    done = 0
    ls = str(usr) + "\t" + str(cname)
    with open(infile, "r+") as f:
        d = f.readlines()
        f.seek(0)
        n = 0
        for i in d:
            if ls not in i:
                f.write(i)
            n += 1
            if ls in i:
                print(str(usr)+" with " + str(cname) + " has been removed from the record")
                done = 1
        f.truncate()
    if done == 0:
        x = "Char not found, try again"
    if done == 1:
        x = "Goodbye, " +str(cname) + " you will be missed."
    print("Usr " + str(usr) + " deleted Char " + str(cname) + " successfully.")
    return x

def delall():
        infile = "dtbot.txt"
        with open(infile,"r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                f.write("")
                print(str(i) + "\t has been deleted")
        f.truncate()
        return "All characters deleted, I hope you're proud of yourself."

# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import datetime
import random
import numpy as np
import testplace as dt

TOKEN = 'NDQ4ODc1MDUxMDIyODExMTM3.DejOgg.3DcQclyDdWNmgQBF0iS905R8iEU'

client = discord.Client()
try: 
    f = open("dtbot.txt", "r+")
except:
    f = open("dtbot.txt", "w")
    f.close()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        
    if message.content.startswith('!!purge') and message.author == "Cap'n#1606":
        abort = input("Continue Purge? y/n")
        if abort == "n":
            arg = "Purge Aborted."
        elif abort == "y":
            arg = dt.delall() 
        msg = arg.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!!reset') or message.content.startswith('!!start'):
        r = message.content.split(" ")
        arg = '{0.author.mention} ' + str(dt.reset(message.author, r[1]))
        msg = arg.format(message)
        await client.send_message(message.channel, msg)
        
    if message.content.startswith('!!quest'):
        r = message.content.split(" ")
        arg = '{0.author.mention} ' + str(dt.quest(message.author, r[1]))
        msg = arg.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!!dt') or message.content.startswith('!!downtime'):
        r = message.content.split(" ")
        arg = "{0.author.mention} " + str(dt.read(message.author, r[1]))
        msg = arg.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!!spend'):
        r = message.content.split(" ")
        if len(r) >= 3:
            x = r[2]
        else:
            x = 1
        arg = "{0.author.mention} " + str(dt.spend(message.author, (r[1]), x))
        msg = arg.format(message)
        await client.send_message(message.channel, msg)
            
    if message.content.startswith('!!help'):
        arg = "Wow, looks like I'm a robot, here to help track your downtime. I have a few major commands, and a few that are so hidden, only my creator, the great and mighty Cap'n#1696 (who spent like 16 hours making me, come on, I add like 2 numbers) knows about them." + "\n" "I'm pretty simple so syntax is important. my main commands follow: ```!!reset [character name] -- will add your character to my database, or resets them, useful if you use all your dt. \n!!dt [character name] -- I'll tell you the number of dt you have. \n!!quest [character name] -- will allow me to start tracking the number of quests you've been on so I can tell you your current dt better." + "\n" +"!!spend [character name] [days spent] -- will tell me you've spent some downtime. If you don't say how many, I'll assume one." +"\n"+"!!delete [character name] -- will delete a character from my database. This cannot be reversed.\n!!syntax will have me tell you the rp syntax, if that's what you want.``` \nthat's all i'm programed to do at the moment. If you have suggestions or comments, including complaints, feel free to send them to Cap'n#1696 who will get round to fixing it at some point. *Happy questing!*"
        msg = arg.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!!syntax'):
        arg = "Hi {0.author.mention} \nI'm here to help you format your rp stuff.\n if you're talking in character remember your quotation marks that look like this " + '"' ". \nIf your character is doing stuff, put it in *italics* do this by putting an asterix * at the start and end of the phrase, make sure there's no space between it otherwise it doesn't work right. \n if your character is thinking, use angular brackets <> \nif you use an ability, use the 'grave accent' that looks like this (it's in the top left of your keyboard, below the escape key) `it makes things look like this` \nthanks for asking for help, there's always more help in the rules book, so refer there. If you're still having problems, ping a dm or admin. \n if you didn't ask for this, message Cap'n#1696, he'll fix me for you, and only for you." 
        msg = arg.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!!delete') or message.content.startswith('!!del'):
        r = message.content.split(" ")
        arg = "{0.author.mention} " + str(dt.delete(message.author,(r[1])))
        msg = arg.format(message)
        await client.send_message(message.channel, msg)
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(datetime.date.today())
    print("Version: " + str(v))
    print('------')

client.run(TOKEN)
