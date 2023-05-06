def red(filename):
    with open(filename, 'r',encoding='utf-8') as f:return f.read()
def ouate(data, filename):
    with open(filename,'w+') as f:f.write(data)


data = [[k for k in x.split("\n") if k] for x in red("shop").split("===") if x]

class Shop_:
	eatable = {}
	def __init__(s,name,info,url,items,alias):
		s.name = name
		s.info = info
		s.url = url
		s.items = items
		s.alias = alias
		s.total = 0
		s.last_tk = ""

	def get_item_name(s):
		return "".join([f"{i+1}. {x.capitalize()}\n" for i,x in enumerate(s.items.keys())])
	def get_item_price(s):
		return "".join([f"{x['price']}:coin:\n" for x in s.items.values()])
	def get_moji(s):
		return [x for x in s.alias.keys()]+["❌"]

def preload_shop(init=False):
	shops = {}
	for shop in data:
		name_shop, cmd_shop = shop[0].rsplit(" ",1)
		info, img_url = shop[1].rsplit(" ",1)
		items,alias = {},{}

		is_food = True if cmd_shop in ["woke", "food"] else False
		for element in shop[2:]:
			moji_choice, item_name = element.split(" ",1)
			item_name,price = item_name.rsplit(" ",1)
			if is_food:
				item_name = item_name.lower()
				Shop_.eatable[item_name]=int(int(price)/15)

			items[item_name] = {"price":int(price),"name":item_name}
			alias[moji_choice] = items[item_name]
		shops[cmd_shop] = Shop_(name_shop,info,img_url,items,alias)

	if init: return Shop_.eatable
	return shops
# print(shops["food"].items["fritents"])

async def load_shop(ctx, discord,bot, choix,argent):

	shops=preload_shop()
	print(shops)
	if not choix in shops : return 0,0,0
	#is_food = True if choix in ["woke", "food"] else False
	shop = shops[choix]

	embed = discord.Embed(title=shop.name,description=shop.info)
	embed.set_thumbnail(url=shop.url)
	embed.add_field(name="Items",value=shop.get_item_name(), inline=True)
	embed.add_field(name="Price",value=shop.get_item_price(), inline=True)

	# def check(msg):
		# return msg.author == ctx.message.author and ctx.message.channel == msg.channel
	
	message =await ctx.send(embed = embed)
	for moji in shop.get_moji(): ##### modifie here
		await message.add_reaction(moji)

	def check_emoji(reaction, user):
		moji = str(reaction.emoji);ok_moji = True if moji in "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣❌" else False
		print(user,ctx.message.author, ok_moji)
		return ctx.message.author == user and message.id == reaction.message.id and ok_moji

	ticket = {}
	def group_items(name):
		if shop.total+shop.items[name]["price"] > argent:
			return "Vous n'avez pas assez\n"+shop.last_tk
		if not name in ticket:
			ticket[name] = {"qty":1,"price":shop.items[name]['price']}
		else:
			ticket[name]["qty"] +=1
		tk = [];total = 0
		for name, objet in ticket.items():
			qty, prix = objet["qty"], objet["price"]
			tk.append(f"x{qty} {name} : {qty*prix:,}:coin:")
			total += qty*shop.items[name]["price"]
		shop.total = total
		tk = [f" Total: {total:>5,}:coin:"]+tk #{total:^45,}
		print(total,"votre arget : ",argent)
		shop.last_tk = "\n".join(tk)
		return "\n".join(tk)

	msg_ticket = await ctx.send("Vos achats : ")
	try:
		while 1:
			reaction,user = await bot.wait_for("reaction_add", timeout=30, check=check_emoji)
			if reaction.emoji =="❌": 
				await ctx.send("Shop closed !")
				break

			achat = ""
			name, price = shop.alias[reaction.emoji]["name"], shop.alias[reaction.emoji]["price"]
			msg = f"{name} pour {price:,}:coin:"
			#set_money(ctx,-price,"add")
			#await set_stealth(ctx,-1)
			tk = group_items(name)
			await msg_ticket.edit(content=tk)#str(group_items(name)))
			await reaction.remove(user)

	except:
		print("exeption cathed")
		await ctx.send("Shop closed !")

	if ticket:
		return ticket,shop.total
	return False,0

