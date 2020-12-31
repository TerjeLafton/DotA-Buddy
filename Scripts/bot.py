import os
import asyncio
from contextvars import ContextVar, Context, copy_context

from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Assigns the Discord token to the TOKEN variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Creates the bot object with a prefix used for all commands given to the bot.
bot = commands.Bot(command_prefix='!')

# Create a Context Variable to tell when the clock should be running and set it to False
clock_running = ContextVar('Clock Running')
clock_running.set(False)
# Create a Context Variable to store the message ID of the initial message created by the bot.
# Used to match the on_reaction_add event to only the message created by the bot
message_id = ContextVar('Message ID')


# Create a on_ready function to say when the bot is ready to go
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# The main bot command to initiate the bots functionality
@bot.command(name='time')
async def time(ctx):
    # Send the initial message, store it in a variable and create reactions
    message = await ctx.send(f'```Match not started yet :( \n\n'
                             f'Click the ✅ to start the match!```')
    await message.add_reaction('✅')
    await message.add_reaction('❎')

    # Store the message ID in the Context Variable created earlier
    message_id.set(message.id)
    print(message_id.get())


# Function to define what happens if anyone reacts to the initial bot message
# We use this to control the clock and such
@bot.event
async def on_reaction_add(reaction, user):
    # Make sure to only look for reactions not made by the bot
    if str(user).split('#')[0] != bot.user.name:
        print(reaction.me)
        print(message_id.get())


bot.run(TOKEN)
