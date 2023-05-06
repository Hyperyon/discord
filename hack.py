from datetime import timedelta
from datetime import datetime
import asyncio as a, random as r
master_key = "> Master Key       : "
trans_key =  "> Transcient Key : "
eapol_mac =  "> EAPOL HMAC : "
time_needed = 0;keys_required = 0
time_passed = 1; keys_tested = 0

async def hack_player(ctx, bot, target='bank'):
    global data
    cars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12345678901234567890"
    sha = r.sample(cars,32)
    ip = ".".join(map(str, (r.randint(0, 255) for _ in range(4))))
    x=[x for x in range(9)];r.shuffle(x);y=x.copy()
    password = [" _"]*len(x)

    console = await ctx.send(".") 
    init = f"> C:\\Users\\scriptKiddie>"
    await console.edit(content=init)

    await a.sleep(1.5)
    init += f"ssh target@{ip}"
    await console.edit(content=init)

    init +=f"\n> ECDSA key fingerprint is SHA256:{''.join(sha)}"
    init+=f"\n> Warning: Permanently added '{ip}' (ECDSA) to the list of know hosts"
    mdp = f"\n> \n> ```target@{ip}'s password: {''.join(password)}```\n"
    prompt = init + mdp


    await a.sleep(1.5)
    await console.edit(content=prompt)
    end = f"> *running brute force script...*"
    prompt = init + mdp + end 
    
    await a.sleep(1.5)
    await console.edit(content=prompt)
    def hide(mdp):
        return "".join([x if not x.isnumeric() else '_' for x in mdp])
    def num(mdp):
        return "".join([x for x in mdp if x.isnumeric()])
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    message = ""
    true_pass = ["x"]*len(x)
    cmd = await ctx.send(".")
    for index in x:
        car = r.choice(cars)
        password[index]  = car
        true_pass[index] = car
        y.pop(0)
        for indice in y:
            password[indice] = r.choice(cars)
        print(password)
        await a.sleep(0.5) #display below
        message = f"> ```{hide(password)}```"
        await cmd.edit(content=message)

        await a.sleep(0.5) # up console display
        prompt = f"{init}\n> \n> ```target@{ip}'s password: {hide(true_pass)}```\n"
        prompt += end
        await console.edit(content=prompt)

    number = num(password)
    turn = 0
    while number and turn <= 14:
        print(turn)
        if number:
            print(number)
            pm= "[+]","[-]"
            prompt =f"{message} *Missing digit please complete*"
            if not turn: await cmd.edit(content=prompt)

            user = await bot.wait_for("message", check=check, timeout=90)
            if user.content == number:break
            if user.content.isnumeric():
                nombre = int(user.content)
                if nombre < int(number): prompt+=f" {pm[0]}"
                if nombre > int(number): prompt+=f" {pm[1]}"
                if nombre == int(number):break

            else:prompt+=" please enter number!"
            
        await cmd.edit(content=prompt)
        turn+=1
    minus_fufu = 20
    mission_success = True

    if turn >= 14 : 
        await cmd.edit(content="Echec de la mission !")
        minus_fufu = 5;mission_success=False

    prompt = f"{init}\n> \n> ```target@{ip}'s password: {''.join(password)}```\n"
    prompt += end
    await console.edit(content=prompt)
    prompt = f"> ```{''.join(password)}``` *password found !*"
    await cmd.edit(content=prompt)
    
    return mission_success,minus_fufu

async def wifi(ctx):
    global time_needed, time_passed,keys_tested,keys_required
    time_needed =r.randint(1500,4200)
    keys_required = time_needed*4512
    time_passed = 1; keys_tested = 0
    reply = await ctx.send('.')
    while time_needed:
        await time_left(reply)
        await a.sleep(3)

    butin = r.randint(150,3500)
    fufu = 10

    stealth = f"\nVous avez perdu {fufu}:detective:"
    return butin, fufu

def get_hex(nb,item):
    nb = str(nb).split('.')
    nb, row = int(nb[0]),int(nb[1])
    hexa = [str(x) for x in range(0,10)]+[x for x in 'ABCDEF']

    tab = []
    item = len(item)+10
    for x in range(row):
        if not x:
            tab+=[' '.join([''.join(r.sample(hexa,2)) for x in range(nb)])]
        else:
            tab+=[' '*item+' '.join([''.join(r.sample(hexa,2)) for x in range(nb)])]

    return '\n> '.join(tab)+'\n'

def display():
    global master_key,trans_key,eapol_mac
    tab = master_key+get_hex(16.1,master_key)
    trans = trans_key+get_hex(16.1,trans_key)
    mac = eapol_mac+get_hex(16.1,eapol_mac)

    return tab+trans+mac

async def time_left(ctx):
    global time_needed, time_passed,keys_tested,keys_required

    time_needed-=r.randint(550,850)
    td = timedelta(seconds=time_passed)
    done = r.randint(450,650)
    keys_tested += done*4512

    msg = "> "+' '*25+'Earthcrack-ng 3.1\n> \n'
    msg +=f"> *[{td}] {keys_tested:,d}/{keys_required:,d} keys tested ({keys_tested/time_passed/2:,.2f} k/s)*\n"

    time_passed+= done

    if time_needed < 0 : time_needed = 0
    td = str(timedelta(seconds=time_needed)).split(':')
    td = f"{td[0]} hour, {td[1]} minutes, {td[2]} seconds"

    msg +=f"> Time left : {td}\n> "
    msg += '\n'+display()+"> ."
    await ctx.edit(content=msg)


def get_embed(d,val=":x: :x: :x: :x:"):
    embed = d.Embed(name="",title="**Serrure de la prison**")
    embed.set_thumbnail(url="https://image.noelshack.com/fichiers/2023/12/3/1679489447-lock.png")
    embed.add_field(name="",value="Trouver la bonne combinaison", inline=True)
    embed.add_field(name="",value=f"\n{val}", inline=0)

    return embed

async def evade(ctx,d,bot):
    code = r.sample(["🔵","🔴","⚪","🟠","🟣","🟡","🟢"],4)
    #code = r.sample(["🔵","🔴","⚪"],3)
    message = await ctx.send(embed=get_embed(d))
    for moji in code:await message.add_reaction(moji)

    r.shuffle(code)  #code becomes good combinaison to find

    def check_moji(reaction,user):
        ok_moji = True if reaction.emoji in "🔵🔴⚪🟠🟣🟡🟢" else False
        return ctx.message.author == user and message.id == reaction.message.id and ok_moji
    
    joueur = []
    while 1:
        try:reaction,user = await bot.wait_for("reaction_add", timeout=30, check=check_moji)
        except:
            await ctx.send("Trop lent!")
            return False
        if not reaction.emoji in joueur: joueur.append(reaction.emoji)
        else: joueur = []
        await reaction.remove(user)

        feedback = "".join(["✅"if code[i]==s else":x:"for i,s in enumerate(joueur)])
        await message.edit(embed=get_embed(d,f"{feedback}\n{''.join(joueur)}"))
        print(feedback)
        if len(feedback) == len(code) and not ":x:" in feedback:
            await ctx.send("Bravo vous avez trouvé")
            return True

