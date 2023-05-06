
import tokken as tok
TOKEN = tok.get_token()

import discord, asyncio as a
from discord.ext import commands, tasks
import requests as req, random as r
import blackjack as white, datetime

CHAN = "casino"
intents = discord.Intents.default()
#intents = discord.Intents.all()
intents.messages = True #v2
#intents.message_content = True #v2
bot = commands.Bot(command_prefix='!', intents=intents,description="Le problème ne sont pas les règles, mais plutôt le cheval")

def red(filename):
    with open(filename, 'r',encoding='utf-8') as f:return f.read()
def ouate(data, filename):
    with open(filename,'w+') as f:f.write(data)

import shop as store

@bot.event
async def on_ready():
    print('bot ready\n')
    check_stealth.start()
    # keep_alive_app.start()
    Player.food_list = store.preload_shop("init")
    print(Player.food_list,"--")

@bot.command()
async def m(ctx, bet=5):
    if not Player.jeton: return 0
    if str(bet).isnumeric(): bet = int(bet)
    else: return 0
    if not Player.set_data(ctx,"money",-bet):return 0
    semaphore()
    result = await white.roll_slots(ctx,bet)
    msg, value = result
    print(f"{value} dans le slibard! {ctx.author}")
    if value: Player.set_data(ctx,"money",value)
    account = Player.set_data(ctx,"money")

    msg = f"{msg} {ctx.author.mention} \n> Argent restant : {account:,}:coin:"
    await ctx.send(msg)
    semaphore()

############## HACK MODULE ##############
import hack as hak
@bot.command()
async def hack(ctx, atk='wifi'):
    if not Player.jeton: return 0

    if atk == 'wifi' :
        semaphore()
        result = await hak.wifi(ctx)
        butin, fufu = result
        stealth = await set_stealth(ctx,fufu)
        money = Player.set_data(ctx,"money",butin)
        await ctx.send(f"{ctx.author.mention} vient de dérober {butin:,}:coin: {stealth}:detective: restant\nArgent restant {money:,}:coin:")
        semaphore()
        return 0

    croupier = "1077200384646455316"
    target = atk[2:-1] if atk[2:-1] != croupier else "bank"

    if not Player.is_member(target):return 0
    else: #atk player

        semaphore()
        Player.last_hack = [str(ctx.author.id),target] #eeeeeee
        print("enter hack mod",str(ctx.author.id),target)
        result, fufu = await hak.hack_player(ctx,bot,target)
        #stealth = Player.set_data(ctx,"fufu",-fufu)

        stealth = await set_stealth(ctx,fufu)
        message = f"\nVous avez perdu {fufu} de furtivité restant {stealth}:detective:"
        if result:
            reward = int(Player.set_data(target,"money") * 0.12)
            if reward > 2_000_000:
                reward = int(2_000_000*0.921)
            Player.set_data(target, "money",-reward)
            account = Player.set_data(ctx,"money",reward)
            message = f"{ctx.author.mention} vient de dérober {reward:,}:coin: {message}"

        await ctx.send(f"{message}")
        semaphore()

############## FURTIVITY MODULE  ##############
async def set_stealth(ctx,delta=10,is_attack=False):
    stealth=Player.set_data(ctx,"fufu",-delta)
    print(int((stealth-100)*(-0.35)))
    if r.randint(0,100) < int((stealth-100)*(-0.35)):
        if is_attack:
            await send_gilbert(ctx,is_attack=True)
        else:
            await send_gilbert(ctx)
    return stealth

async def send_gilbert(ctx,is_poucave = False,is_attack = False):
    ctx_ = ctx
    if is_poucave:ctx = is_poucave
    Player.set_data(ctx,"is_jail",maintenant()+900) 
    Player.set_data(ctx,"fufu",-25)
    gif = "<a:gyro:1082383574562521219>"
    crs = "<:fusil:1069939818504650782>"
    fine = int(Player.set_data(ctx,"money")*0.20)
    fine = fine if fine < 850_000 else 850_000
    if is_attack:fine=10_000
    Player.set_data(ctx,"money",-fine)
    Player.save_data()
    message = f"\n\n{gif}__**SECURITY ALERT attack has been detected**__{gif}"
    message += f"\n Gilbert has caught you !!{crs}\n A fine of {fine:,d}:coin: has been applied "
    ctx = ctx_
    await ctx.send(message)

@bot.command()
async def taunt(ctx,target="fake"):

    if not target: return 0
    victim = str(target[2:-1]);print(victim)
    if not Player.is_member(victim) : return 0
    semaphore()
    damage = r.choice([1,1,1,1,2])

    target = await bot.fetch_user(int(victim))
    before_damage = Player.set_data(victim,"vie")
    victime = Player.set_data(victim,"vie",-damage)
    if victime > before_damage:
        await ctx.send(f"{target.mention} a succombé de ses blessures, il s'est réincarné")
    message = f"Vous venez d'infliger {damage}:crossed_swords: à {target.mention}\n*-10:detective:*"
    message+= f"\nVie restante de votre victime : {victime}:heart:"
    await ctx.send(message)
    await set_stealth(ctx,is_attack=True)
    semaphore()

############## SHOP MODULE ##############
@bot.command()
async def shop(ctx, arg="food"):
    if not Player.jeton:return 0
    semaphore()
    money = Player.set_data(ctx,"money")
    tk,depense = await store.load_shop(ctx, discord,bot,arg,money)
    if not tk : 
        semaphore()
        return 0
    Player.set_data(ctx,"item",tk)
    Player.set_data(ctx,"money",-depense)
    # for key,objet in tk.items():
        # print(key,objet["price"],objet["qty"])
    semaphore()

@bot.command()
async def debug(ctx):
    if not Player.jeton: Player.jeton = True


import json
############## TRANSFERT MODULE ##############
@bot.command()
async def give(ctx, target='none',amount='none'):
    if target == 'none' or amount =='none':return 0
    if not amount.isnumeric(): return 0
    if str(ctx.author) == target : return 0
    if not "@" in target: return 0

    target = str(target[2:-1])
    amount = int(amount)

    if not Player.is_member(target):
        Player.create_account(target)

    tax = int(amount*0.1)
    transfert_money = amount-tax
    Player.set_data(ctx,"money",-amount)
    Player.set_data(target,"money",transfert_money)

    target_ = await bot.fetch_user(int(target))
    print(f'{target_} receive {amount} gold from {ctx.author}')

    msg = f"Vous venez d'envoyer {amount:,d}:coin:\n"
    msg += f"{tax:,d}:coin: de frais ont été appliqués"
    await ctx.reply(msg)

    Player.set_data(target,"pseudo",target_.name)
    Player.save_data()


from datetime import datetime
def maintenant():return int(round(datetime.timestamp(datetime.now())))

class Player:
    food_list = None
    jeton = True;last_hack = ['fake','fake']
    cmd_on_wait = []
    a = "id money pseudo atk def fufu is_jail".split()
    data = json.loads(red("bdd"))

    def cmd_queue(ids,cmd):
        print(ids.author.name)
        Player.cmd_on_wait.append([ids,cmd])
        print(Player.cmd_on_wait)

    def can_revenge(ids): #atk, target
        ids = str(ids.author.id)
        if ids == Player.last_hack[1]: return True
        else:return False

    def set_data(ids,attribut,value=None):
        # if attribut not in a:
        #     print("error attr no found")
        #     return 0 
        #is_mention = True if not ids isinstance(ids,str) else False
        ids = ids if isinstance(ids, str) else str(ids.author.id)
        if value is None: #get_data
            return Player.data[ids][attribut]

        if not ids in Player.data: Player.create_account(ids)

        if attribut == "money":
            if isinstance(value, str) and not value.isnumeric() : return 0
            value = int(value)
            if value < 0 and Player.data[ids][attribut] < abs(value): #minus money
                print("not enough money")
                return 0
            else:
                print("transaction done")
                Player.data[ids][attribut] += value
        #else: return 0

        elif attribut == "fufu":
            Player.data[ids]["fufu"] += value
            if Player.data[ids]["fufu"] > 100:Player.data[ids]["fufu"] = 100
            if Player.data[ids]["fufu"] < -100:Player.data[ids]["fufu"] =-100

        elif attribut == "faim":
            Player.data[ids]["faim"] += value
            if Player.data[ids]["faim"] > 100:
                Player.data[ids]["faim"] = 100
                pdm = (100-value)*0.005
                Player.data[ids]["poids"] = round(pdm +Player.data[ids]["poids"],2)
            if Player.data[ids]["faim"] < 0:
                Player.data[ids]["faim"] = 0
                Player.data[ids]["poids"] = round(value*0.01 + Player.data[ids]["poids"],2)
            poids = Player.data[ids]["poids"]
            if poids > 85 or poids < 55:
                Player.data[ids]["vie"] -= r.choice([1,1,1,2,2,3])

        elif attribut == "fatigue":
            membre = Player.data[ids]
            Player.data[ids][attribut]+=value
            if membre["fatigue"] > 100:membre["fatigue"] = 100
            if membre["fatigue"] < 0:membre["fatigue"] =0

        elif attribut in ["force","poids","vie","grade","evade"]:
            Player.data[ids][attribut]+=value            
            if attribut in ["grade","evade"]:
                Player.data[ids][attribut]= round(Player.data[ids][attribut],1)
            if attribut=="poids":
                Player.data[ids][attribut]= round(Player.data[ids][attribut],2)
            if attribut == "vie":
                if Player.data[ids]["vie"] <= 0:
                    pseudo = Player.data[ids]['pseudo']
                    print(f"{pseudo} est mort")
                    Player.data[ids] = Player.data["new"]
                    Player.data[ids]["pseudo"] = pseudo

        elif attribut == "item" and isinstance(value, dict):
            player_items = Player.data[ids]["item"]
            for name,objet in value.items():
                print(name,objet["price"],objet["qty"])
                if name in player_items:
                    player_items[name]+=objet["qty"]
                else:
                    player_items[name] = objet["qty"]
            print(player_items)



        else: #be careful for other stat of player !!!
            Player.data[ids][attribut] = value

        return Player.data[ids][attribut]

    def create_account(new_id):Player.data[new_id] = Player.data["new"].copy()

    def is_member(ids):
        ids = ids if isinstance(ids, str) else str(ids.author.id)
        return True if ids in Player.data else False

    def save_data():
        ouate(json.dumps(Player.data,indent=4, sort_keys=1),"bdd")
        print("===bdd saved!===")

    def semaphore():
        Player.jeton = False if Player.jeton else True
        output = "sem lock" if not Player.jeton else "sem unlock"
        if Player.jeton:
            Player.save_data()
        print(output)
#1069010938918867065 id general chan
############## QUOTES MODULE ###############
import quote
semaphore = Player.semaphore
@bot.command()
async def vdm(ctx):
    if not Player.jeton: return
    semaphore()#Player.semaphore()
    await quote.vdm(ctx)
    semaphore()

@bot.command()
async def dodo(ctx):
    if not Player.jeton: return
    semaphore()
    await quote.dodo(ctx)
    semaphore()


@bot.command() ####dddddd
async def ddd(ctx):
    print(Player.set_data(ctx,"grade"))
    print(Player.set_data(ctx,"grade",0.1))

def get_level(stat):return int(str(stat).split(".")[0])

@bot.command()
async def work(ctx):
    grade = get_level(Player.set_data(ctx,"grade"))
    pay = 2000*grade
    tax = int(pay * 0.2)
    net_pay =pay - tax

    if Player.set_data(ctx,"fatigue") + 35 > 100 or Player.set_data(ctx,"faim")-25 < 0:
        await ctx.send("Condition non requise")
        return 0
    semaphore()
    Player.set_data(ctx,"fatigue",35)
    Player.set_data(ctx,"money",net_pay*grade)
    Player.set_data(ctx,"faim",-25)
    Player.set_data("bank","money",tax)
    grade= Player.set_data(ctx,"grade",0.1)
    semaphore()
    message = f"Grade : {grade}\nVous avez gagné {net_pay:,}:coin: et payé {tax:,}:coin: d'impôts"
    message +=f"\n+35:tired_face: et -25:meat_on_bone:"
    await ctx.send(message)

@bot.command()
async def eat(ctx):
    item_consumed,food_value,food_level = consume_food(ctx)

    semaphore()
    if not item_consumed:
        await ctx.send("Vous n'avez rien à manger chez vous!")
        semaphore()
        return 0

    message = f"> Vous avez consommé x1 {item_consumed} et récupéré {food_value}:meat_on_bone:"
    message +=f"\n> Niveau de nourriture : {food_level}:meat_on_bone:"
    await ctx.send(message)
    semaphore()

def consume_food(member):
    food_value = Player.food_list
    player_items = Player.set_data(member,"item")
    player_food = [x for x in player_items.keys() if x.islower() and x in food_value]
    if not player_food: return False,0,0

    item_consumed = player_food.pop(0)
    food_value = food_value[item_consumed]
    player_items[item_consumed]-=1
    if not player_items[item_consumed]:player_items.pop(item_consumed)
    food_level = Player.set_data(member,'faim',food_value)

    return item_consumed,food_value,food_level


def minus_food(member):
    faim = Player.set_data(member,"faim",-8)
    if faim < 21:
        if not consume_food(member):
            spent = Player.set_data(member,"money",r.randint(350,3500)*-1)
            Player.set_data(member,"faim",int(spent/25))

def minus_fatigue(member):Player.set_data(member,"fatigue",-25)

@bot.command()
async def muscu(ctx):
    fatigue = Player.set_data(ctx,"fatigue")
    if fatigue + 50 > 100:
        await ctx.send("Vous êtes trop fatigué pour go muscu")
        return 0
    semaphore()
    tired = Player.set_data(ctx,"fatigue",50)
    force = Player.set_data(ctx,"force",1)
    lost_weight = r.randint(250,350)*-0.001
    food_consume = r.randint(10,30)
    Player.set_data(ctx,"poids",lost_weight)
    Player.set_data(ctx,'faim',)
    message=f"Vous avez gagné 1:muscle: et obtenez {tired}:tired_face:"
    message+=f"\nNourriture consommée : {food_consume}:meat_on_bone:"
    await ctx.send(message)
    semaphore()


@bot.command() #wwwwwwww
async def eva(ctx,arg="none"):
    if Player.set_data(ctx,"is_jail") == "free":return 0
    if Player.set_data(ctx,"faim")-20 < 0:
        await ctx.send("Vous n'avez pas assez d'énergie")
        return 0
    Player.set_data(ctx,"faim",-20)
    Player.set_data(ctx,"fatigue",20)
    if await hak.evade(ctx,discord,bot):
        semaphore()
        Player.set_data(ctx,"is_jail","free")
        Player.set_data(ctx,"evade",0.1)
        agi = Player.set_data(ctx,"evade")
        msg = f"Bien joué vous vous êtes évadé !\nLvl agi :{agi}:smirk_cat:"
        msg += f"\n-20:meat_on_bone: +20:tired_face:"
        await ctx.send(msg)
        semaphore()

@tasks.loop(minutes=1)
async def check_stealth():
    print("enter loop check")
    if datetime.now().strftime("%M") != "41": return 0
    if not Player.jeton: return 0
    print("time show !!")
    semaphore()
    for id_member, row in Player.data.items():
        member = Player.data[id_member]
        is_jail=str(member["is_jail"]).isnumeric()
        if is_jail and int(member["is_jail"]) < maintenant():
            member["is_jail"] = "free"
            is_jail = False
        if not is_jail:
            z= Player.set_data(id_member,"fufu",10)
            print(z, id_member, member["pseudo"])
        minus_food(id_member) #index = member id
        minus_fatigue(id_member)
        Player.set_data(id_member,"vie",0)
    semaphore()

@bot.event
async def on_command_completion(ctx):
    print("comd check")
    while len(Player.cmd_on_wait):
        context, commande = Player.cmd_on_wait.pop(0)
        print(commande)
        cmd = bot.get_command(commande)

        arg = commande.split()[-1]
        if len(commande.split()) == 2:
            await cmd(context,arg)
        else:
            await cmd(context)
        await a.sleep(1.8)
        print("old cmd done")

count = 0
import ai
@bot.event 
async def on_message(msg):
    global count
    if msg.channel.name != CHAN:return 0
    cmd = [x.name for x in bot.commands]
    user_cmd = msg.content[1:]

    if not Player.jeton and "!" in msg.content and  user_cmd.split()[0] in cmd:
        pass#ctx = await bot.get_context(msg)
        #Player.cmd_queue(ctx, user_cmd)

    if str(msg.author.id) == "1077200384646455316":return 0
    print(msg.author.name)

    if str(msg.author.id) == "533736011407294465" and "free" in msg.content:
        Player.set_data(msg,"is_jail","free")
        await msg.channel.send(f"{msg.author.name} utilise l'immunité diplomatique")

    if "!" in str(msg.content) and str(Player.set_data(msg,"is_jail")).isnumeric():
        if Player.set_data(msg,"is_jail") < maintenant():
            message = "Soyez plus malin la prochaine fois ;-)"
            Player.set_data(msg,"is_jail","free")
            Player.save_data()

        elif "eva" in msg.content:
            ctx = await bot.get_context(msg)
            await ctx.invoke(eva)
            message = "."
        else: 
            message ="Vous êtes en détention, vous ne pouvez rien faire"
        await msg.channel.send(message)
        return 0
    
######### OPEN AI MODULE ##############
    if not Player.jeton: return 
    # if count < 50 and 'croupier' in str(msg.content).lower():
    #         semaphore()
    #         count +=1;print(count)
    #         await ai.ai(msg,bot)
    #         semaphore()

    await bot.process_commands(msg) #avoid blocking cmd because of ai


##### BLACK JACK ######
@bot.command()
async def b(ctx, arg=5):    
    if not Player.jeton: return
    if str(arg).isnumeric(): arg = int(arg)
    else: return 0
    if Player.set_data(ctx,"money",-arg):
        semaphore()
        result = await white.blackjack(ctx,discord,bot,int(arg))
        if result:
            Player.set_data(ctx,"money",result)
        print(Player.set_data(ctx,"money"))
        semaphore()


#### bank balance cmd ####
@bot.command()
async def stat(ctx):
    if not Player.is_member(ctx): return 0
    money = Player.set_data(ctx,"money")
    fufu = Player.set_data(ctx,"fufu")

    message = f"""> Argent disponible : {money:,d}:coin:"""
    message += f"\n> Vie : {Player.set_data(ctx,'vie')}:heart:"
    message += f" Furtivité : {fufu}:detective:"
    message += f"\n> Nourriture : {Player.set_data(ctx,'faim')}:meat_on_bone:"
    message += f" Fatigue : {Player.set_data(ctx,'fatigue')}:tired_face:"
    message += f"\n> Force : {Player.set_data(ctx,'force')}:muscle:"
    message += f" Poids : {Player.set_data(ctx,'poids')}kg"
    await ctx.channel.send(message)


@bot.command()
async def revenge(ctx):
    print(Player.last_hack[0])
    if Player.can_revenge(ctx):
        #result, fufu = await hak.hack_player(ctx,bot,Player.last_hack[0])
        victim = Player.last_hack[0]
        Player.set_data(victim,"fufu",-30)

        butin = int(Player.set_data(victim,"money")*0.3)
        Player.set_data(victim,"money",-butin)
        Player.set_data(ctx,"money",butin)
        message = f"Vous venez de contre-attaquer, vous avez récupéré {butin:,}:coin:"
        message += f"\n Argent disponible {Player.set_data(ctx,'money')}:coin:"
        await ctx.send(message)
        Player.last_hack = ["fake","fake"]


@bot.command()
async def poucave(ctx):
    if not "fake" in Player.last_hack:
        victim = Player.last_hack[0]
        #Player.set_data(victim)
        Player.last_hack = ["fake","fake"]
        await send_gilbert(ctx,victim)

    
######## DOWN CMD ###########
import os

@bot.command()
async def free(ctx,target="non"):
    if ctx.author.id != "533736011407294465": return 0

    if target != "non":
        target = str(target[2:-1])
        Player.set_data(target,"is_jail","free")

    else:
        Player.set_data(ctx,"is_jail","free")
    await ctx.send(f"{ctx.author.name} utilise l'immunité diplomatique")
    Player.save_data()


@bot.command()
async def reboot(ctx):
    if ctx.author.id != 533736011407294465: return 0
    await ctx.channel.send('Arrivederci ! and hello')
    await ctx.bot.logout()
    os.popen('python3 bot.py &')
    await a.sleep(5)

@bot.command()
async def down(ctx):
    if ctx.author.id != 533736011407294465: return 0
    await ctx.channel.send('Arrivederci !')
    await ctx.bot.logout()

bot.run(TOKEN)
