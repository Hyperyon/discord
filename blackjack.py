import random as r, asyncio as a

stickers = {'pasteque':'<:c1:1077242304806531142>',
'ananas':'<:c2:1077242317473321071>',
'coco':'<:c3:1077242327510290543>',
'citron':'<:c5:1077242350688018613>',
'pomme':'<:c6:1077242412470120518>',
'leetchi':'<:c4:1077242338411286660>',
'banane':'<:banahi:1075042696261025882>'}

stickers_ = '<a:roll1:1077504541831999499><a:roll2:1077515045652668417><a:roll3:1077513261056016384>'
stickers_list = list(stickers.keys())

async def roll_slots(ctx,mise):
    reply = await ctx.send('.') 
    await reply.edit(content=stickers_)
    await a.sleep(5)
    rolling = [get_sticker(),get_sticker(),get_sticker()]
    await reply.edit(content=stickers[rolling[0]]+stickers[rolling[1]]+stickers[rolling[2]])

    return is_duplicate(rolling,mise)

def get_sticker(): return r.choice(stickers_list)

def is_duplicate(liste,bet):
    match = list(set(liste))
    slot = ' '.join(liste);msg,value = '',False

    if len(match) == 1 and 'banane' in match: 
        value = 200*int(bet/5)
        msg = f"*JACKPOT !!! you win {value:,d}*"
    elif len(match) == 1:
        value = 100*int(bet/5)
        msg = f"*Nice! you win {value:,d}*"
    elif slot.count('banane') == 2:
        value = 40*int(bet/5)
        msg = f"*you win {value:,d}*"
    elif slot.count('banane') == 1:
        value = 20*int(bet/5)
        msg  = f"*you win {value:,d}*"
    else:
        msg = f"Perdu! vous venez de faire un don de {bet:,d} :coin: à la banque"

    return msg,value

paquet = {}
croupier,player = [],[]
bank_hand, player_hand = 0,0
value = 2
boucle = True
chiffres = [str(x) for x in range(2,10)]+['valet','dame','roi','as']
symboles = ['♠️','♥️','♣️','♦️'];cartes = []

for symbole in symboles:
    for chiffre in chiffres:
        cartes += [chiffre+symbole]

for carte in cartes:
    paquet[carte] = value if value < 10 else 10
    if 'as' in carte: 
        paquet[carte]+=1
        value = 1
    value+=1
    if value == 14:value = 1

cartes *= 20

def get_embed(d,val="> Main banque :\n> Main joueur :"):
    embed = d.Embed(name="",title="**Partie de blackjack**")
    #embed.set_thumbnail(url="https://image.noelshack.com/fichiers/2023/12/3/1679489447-lock.png")
    embed.add_field(name="",value="", inline=True)
    embed.add_field(name="",value=f"\n{val}", inline=0)
    return embed

async def blackjack(ctx,d,bot,arg=5):
    global croupier, player, paquet, bank_hand, player_hand,boucle
    player_bet = arg
    #await ctx.send(f"\nPartie de {ctx.author.mention}")
    message = await ctx.send(embed=get_embed(d))
    button = ["🆗","✋"]
    for moji in button:await message.add_reaction(moji)

    resultat = await ctx.send("*🆗 pour piocher ✋ pour passer*")

    for x in range(2):
        croupier.append(pick_card())
        player.append(pick_card())
    turn= 1;texte = f'You loose {player_bet:,d}:coin:'
    await check_hand(turn,d,message)

    if player_hand==21:
        boucle = False
        texte = f'blackjack ! player win {player_bet*4:,}:coin:'
        player_bet += 4*arg

    def check_moji(reaction,user):
        ok_moji = True if str(reaction.emoji) in "🆗✋" else False
        return ctx.message.author == user and message.id == reaction.message.id and ok_moji
    
    while boucle:
        turn +=1;user = ''
        try:reaction,user = await bot.wait_for("reaction_add", timeout=15, check=check_moji)
        except a.TimeoutError:
            await ctx.channel.send("Timeout!")
            return False
        
        await reaction.remove(user)

        if user:
            if reaction.emoji == '🆗':
                player.append(pick_card())
            await check_hand(turn,d,message)

            if player_hand == 21:
                texte = f'blackjack ! player win {player_bet*4:,}:coin:'
                player_bet += 4*player_bet
                break
            if player_hand > 21:
                print('player loose')
                player_bet = False
                break
            
            if bank_hand == 21:
                texte = f'croupier win !u give him {player_bet:,}:coin:'
                player_bet = False
                break

            if player_hand >= bank_hand and bank_hand < 21:
                croupier.append(pick_card())
                await check_hand(turn,d,message)

            if bank_hand > 21:
                texte = f'you win {player_bet*2:,}:coin:'
                player_bet += player_bet*2
                break
        
        else:break

    await resultat.edit(content=texte)   
    player_hand,bank_hand = 0,0
    croupier, player = [],[]
    boucle = True
    return player_bet


def pick_card():
    global cartes
    card = r.choice(cartes)
    cartes.remove(card)
    #print('\n\nnb de carte restantes ',len(cartes))
    return card,paquet[card]

def add_val(hand):return sum([x[1] for x in hand])

async def check_hand(turn,d,reply):
    global bank_hand,player_hand,boucle
    player_hand, bank_hand = add_val(player),add_val(croupier)
    texte = f'> [{player_hand}] main joueur {[x[0] for x in player]}\n'
    if turn == 1:
        texte += f'> [{croupier[0][1]}] main croupier {croupier[0][0]}'
    else:
        texte += f'> [{bank_hand}] main croupier {[x[0] for x in croupier]}'
    if player_hand == 21 : boucle = not boucle
    await reply.edit(embed=get_embed(d,texte))
