import requests as req
import html

def red(filename):
    with open(filename, 'r',encoding='utf-8') as f:return f.read()
def ouate(data, filename):
    with open(filename,'w+') as f:f.write(data)


def get(url):return req.get(url).content.decode('utf-8')
def get_vdm():
    url='https://www.viedemerde.fr/aleatoire'
    start_tag = 'block text-blue-500 dark:text-white my-4'
    end_tag = "VDM"
    source = [x.split(end_tag)[0].split('\n')[1]+'VDM' for x in get(url).split(start_tag)[1:]]
    vdm = [html.unescape(x) for x in source]
    new_data = '\n'.join(vdm)+'\n'
    ouate(new_data,'vdm')


async def vdm(ctx):
    data = [x for x in red('vdm').split('\n') if 'VDM' in x]
    if len(data) > 0:
        vdm = '> '+data.pop()
        await ctx.send(vdm) 
        new_data = '\n'.join(data)+'\n'
        ouate(new_data,'vdm')
    if not len(data):get_vdm()

    print('vdm left : ',len(data))


async def dodo(ctx):
    dodo = [x for x in red('dodo').split('\n') if x]
    if len(dodo) > 0:
        quote = '> '+dodo.pop()
        await ctx.send(quote)
        data = '\n'.join(dodo)+'\n'
        ouate(data, 'dodo')

    if not len(dodo): get_dodo()

def get_dodo():
    start_tag = 'anecdote-content-wrapper'
    other_tag = '<a href="/'
    end_tag = '<span class="read-more">'
    url = 'https://secouchermoinsbete.fr/random'

    data = [x.split(end_tag)[0].split(other_tag)[1] for x in get(url).split(start_tag)[1:]]
    data = [html.unescape(x.split('">')[1]).strip() for x in data if not 'premium-needed' in x]
    data = '\n'.join(data)+'\n'
    ouate(data, 'dodo')