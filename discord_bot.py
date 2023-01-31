import discord as ds
from discord import app_commands
from discord.ext import commands
import MKTBAPI as api

bot = commands.Bot(command_prefix="!", intents=ds.Intents.all())
token = "Hidden for your and my safety."

@bot.event
async def on_ready():
    print('Bot is Live.')
    try:
        synced = await bot.tree.sync()
        print("Synced {} command(s)".format(len(synced)))
    except:
        print("error with sync")    


@bot.tree.command(name="submit")
@app_commands.describe(table_id = "String of #s sent when table is first created.")
@app_commands.describe(division = "Divison you are currently playing for.")
async def submit(interaction: ds.Interaction, table_id: str, division: str):
    await interaction.response.send_message("Submitting... Please wait a moment.", delete_after=5)
    api.main(table_id, division) #function ran
    await interaction.followup.send(content=f"Submitted **Divison {division}** match with ID **{table_id}** to the Analytics Team!",)
    
bot.run(token)
