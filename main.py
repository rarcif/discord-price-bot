import os
import discord
import requests
from keep_alive import keep_alive

# discord commands
    # !help   prints list of commands
    # !price  prints current price

###########
# variables 
###########
COIN = "crypto-com-chain" # coin ID - coincecko
CURRENCY = "usd" # currency conversion
BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
TVL = "total_value_locked"
MARKET = "market_data"

################
# price endpoint 
################
PRICE_ENDPOINT = f"https://api.coingecko.com/api/v3/simple/price?ids={COIN}&vs_currencies={CURRENCY}" # endpoint - coingecko
req = requests.get(url = PRICE_ENDPOINT) # request endpoint data
price = req.json()[COIN][CURRENCY] # convert data into json

###############
# TLV endpoint 
###############
TLV_ENDPOINT = f"https://api.coingecko.com/api/v3/coins/{COIN}"
req = requests.get(url = TLV_ENDPOINT) # request endpoint data
tvl = req.json()[MARKET][TVL][CURRENCY]# convert data into json

###########
# functions
###########

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

  # list commands
  if message.content.startswith('!help'):
    await message.channel.send('Command List: \n [!help] - prints the list of commands \n [!price] - prints the current CRO price \n [!tvl] - prints the total value locked'')

  # list current price 
  if message.content.lower() == "!price":
    await message.channel.send(f'The current price of CRO is: {price} USD')

  # list total value locked
  if message.content.lower() == "!tvl":
    await message.channel.send(f'The total value locked of CRO is: {tvl} USD')

keep_alive() # keep server alive

client.run(BOT_TOKEN)