import discord
import requests
from replit import db
from keep_alive import keep_alive

# discord commands
    # !help   prints list of commands
    # !price  prints current price

# variables
token = "crypto-com-chain" # CRO token variable 

# getting crypto data 
def getData(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd' # crypto data endpoint
  req = requests.get(url = URL) # request url to fetch data
  data = req.json() # convert into json payload
  # print(data) 

  # putting the crypto data into db
  for i in range(len(data)):
    db[data[i]['id']] = data[i]['current_price']

  if crypto in db.keys(): 
    return db[crypto]
  else:
    return None

# send discord notificaiton to a channel
async def sendMessage(message):
  await discord.utils.get(client.get_all_channels(),name='general').send(message)

# instantiate a discord client
client = discord.Client()

@client.event
async def on_ready():
  print(f'You have logged in as {client}')
  channel = discord.utils.get(client.get_all_channels(),name='general')

  await client.get_channel(channel.id).send('bot is now online!')

# called whenever there is a message in the chat
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!help'):
    await message.channel.send('Command List: \n  !help     prints the list of commands \n  !price     prints the current CRO price')

  # list current price 
  if message.content.lower() == "!price":
    await message.channel.send(f'The current price of CRO is: {getData(token)} USD')

keep_alive()

BOT_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
client.run(BOT_TOKEN)