import os
import discord
import requests
from keep_alive import keep_alive

# discord commands
    # !help   prints list of commands
    # !price  prints current price

# variables
coin = "crypto-com-chain" # coin ID - coincecko
currency = "usd" # currency conversion
endpoint = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}" # endpoint - coingecko
req = requests.get(url = endpoint) # request endpoint data
data = req.json()[coin][currency] # convert data into json

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
    await message.channel.send(f'The current price of CRO is: {data}')

keep_alive() # keep server alive

BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
client.run(BOT_TOKEN)