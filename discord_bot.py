"""
GSC Match Submission Bot - Discord Interface
A program for users to send data from their matches via a Discord Bot
Made by: Alex Keys
"""

#IMPORTS
import discord as ds
from discord import app_commands
from discord.ext import commands
import MKTBAPI as api

#BOT INFORMATION
bot = commands.Bot(command_prefix="!", intents=ds.Intents.all())
token = "Hidden for my safety."

#BOT INITIALIZATION
@bot.event
async def on_ready():
    print('Bot is Live.')
    try:
        synced = await bot.tree.sync()
        print("Synced {} command(s)".format(len(synced)))
    except:
        print("error with sync")    

#'Submit' COMMAND: players enter in their Table Bot ID & their GSC Division and the data from the ID gets stored into .txts 
@bot.tree.command(name="submit")
@app_commands.describe(table_id = "String of #s sent when table is first created.")
@app_commands.describe(division = "Divison you are currently playing for.")
async def submit(interaction: ds.Interaction, table_id: str, division: str):
    await interaction.response.send_message("Submitting... Please wait a moment.", delete_after=5)
    api.main(table_id, division) #function ran
    await interaction.followup.send(content=f"Submitted **Divison {division}** match with ID **{table_id}** to the Analytics Team!",)

#TURNING ON THE BOT
bot.run(token)
