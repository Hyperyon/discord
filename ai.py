import openai, tokken as tok, random as r
openai.organization = "org-W0Tmu2PTgpU6kRhTT0qxRYEy"
openai.api_key = tok.ai_token()

emotions = {
    "joyeux":'<:penche:1069219530775212032>',
    "rire": '<:ayaa:1069945364062404689>',
    "blasé":'<:bordel:1069884342244999178>',
    "triste":'<:hin:1014130558818848808>',
    "énervé":'<:ouga:1052130604084379668>',
    "colère":'<:ouga:1052130604084379668>',
}

feel_request = """Choisir un mot pour décrire le paragraphe en haut dans cette liste suivante : 
triste, blasé, rire, joyeux, énervé, colère. Si aucun ne correspond tu écris 'tabernake'"""

flag_request = False


async def ai(msg,bot):
    print('reçu une notif')
    reply = await send_request(str(msg.content).replace('croupier',' '))
    if reply:

        if r.choice([True,True,True,False]): 
            feel_req = '"'+str(msg.content)+'"\n\n'+feel_request
            while flag_request:pass

            feeling = await send_request(feel_req)
            feeling = feeling.lower()
            print(feeling,'<------')
            for feel in emotions.keys():
                print('check ',feel)
                if feel in feeling:
                    reply+=' '+emotions[feel]
                    print(reply)
                    print(feel)
                    break
        await msg.reply(reply)

async def send_request(prompt):
    global flag_request
    __ =''
    if len(prompt) > 0:
        flag_request = True

        __ = openai.Completion.create(engine="text-davinci-003", prompt=str(prompt), max_tokens=185,)["choices"][0]["text"]
    else: __ = False
    flag_request = False
    return __