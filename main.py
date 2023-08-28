import discord
from discord import Embed
from colorama import Fore
from pymongo.mongo_client import MongoClient
from discord.ext import commands
from datetime import datetime
import json
import os

uri = os.environ['mongo_url']
client = MongoClient(uri)
db = client["Database"]
colliction = db["tashher"]

with open('./config.json', "r") as f:
    c = json.load(f)

try:
    client.admin.command('ping')
    print(f"{Fore.CYAN}Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{Fore.YELLOW}This Bot developed by devM7MD")
    print(f"{Fore.GREEN}Connected to {bot.user}{Fore.RESET}.")

@bot.event
async def on_member_join(member:discord.Member):
    MemberEmbed = Embed(
                title="تشهير بوت",
                description=f"Hello {member.mention} I'm tashher bot developed by devM7MD\nIf you need like this bot just click the following button or send friend to -> **its.m7md.** I have good prices for all bot\ndevM7MD is a Full-stack web developer",
                color=discord.Color.random()
            )
    btn_view = discord.ui.View()
    btn = discord.ui.Button(label="its.m7md.", style=discord.ButtonStyle.link, disabled=False, url="https://discord.com/users/992111921048342611")
    btn_view.add_item(btn)
    member_dm = await member.create_dm()
    # check = member_dm.can_send()
   # if check == True:
    await member_dm.send(embeds=[MemberEmbed], view=btn_view)
   # if check == False:
      #  print(f"I can't send message to this user {member.metion}")

@bot.slash_command(name="ping", description="Show the ping of the bot")
async def ping(ctx:discord.ApplicationContext):
    await ctx.defer()
    ping = round(bot.latency * 1000)
    pingEmbed = Embed(title="Pong!", color=discord.Color.random(), description=f"**Pong! :ping_pong: {ping}ms**")
    pingEmbed.set_footer(text="Developed by devM7MD | 'its.m7md.'")
    await ctx.respond(embeds=[pingEmbed])


@bot.slash_command(name="add-user")
@discord.option(name="user", description="The user you need add it to database", required=True)
@discord.option(name="reason", description="reason of why you add this user in the database", required=True)
# @commands.has_permissions(administrator=True)
async def add_user(ctx:discord.ApplicationContext, user:discord.User, reason):
    if ctx.user.id not in c["owners"]:
        await ctx.respond("**Sorry You Don't have permission to use this command :x:**")
        return
    await ctx.defer()
    if user.id == ctx.user.id:
        await ctx.respond("**You can't add your self to the database**")
    check = colliction.find_one({"_id":user.id})
    # print(f"check from add_user (if check) ->\n{check}")
    if check == None:
        dic = {
               "_id":user.id,
               "reason":reason,
               "adding_time":datetime.utcnow()
          }
        colliction.insert_one(dic)
        await ctx.respond("**User is successfully added to database :white_check_mark:**")
    if check != None:
        embed = Embed(
                title="User Already Found",
                description=f"""user_id : {user.id}\nuser_name : {user.name}\nreason : {check['reason']}\nAdding_date : {datetime.utcnow()}""",
                color=discord.Color.random()
            )
        embed.set_footer(text="Developed by devM7MD | 'its.m7md.'")
        await ctx.respond(embeds=[embed])

@bot.slash_command(name="check", description="Check If any user in the database")
@discord.option(name="user", description="the user you need to check if this user in database")
async def check_user(ctx:discord.ApplicationContext, user:discord.User):
    await ctx.defer()
    check = colliction.find_one({"_id":user.id})
    if check:
        # print(check)
        embed = Embed(title="User is Found",
                      description=f"""user_id : {user.id}\nuser_name : {user.name}\nreason : {check['reason']}\nAdding_date : {datetime.utcnow()}""",
                      color=discord.Color.random())
        embed.set_footer(text="Developed by devM7MD | 'its.m7md.'")
        await ctx.respond(embeds=[embed])
    if not check:
        embed = Embed(title="User is not Found", description="This User not in saved in the database but this don't mean we trust him/her .")
        embed.set_footer(text="Developed by devM7MD | 'its.m7md.'")
        await ctx.respond(embeds=[embed])

@bot.slash_command(name="remove", description="removing the user you select from the database")
# @commands.has_permissions(administrator=True)
async def remove_user(ctx:discord.ApplicationContext, user:discord.User):
    if ctx.user.id not in c["owners"]:
        await ctx.respond("**Sorry You Don't have permission to use this command :x:**")
        return
    if user.id == ctx.user.id:
        await ctx.respond("**You can't remove your self from the database**")
        return
    await ctx.defer()
    check = colliction.find_one({"_id":user.id})
    if check == None:
        await ctx.respond("**Sorry this user was not found in the database :x:**")
    if check != None:
        colliction.delete_one(check)
        await ctx.respond(f"**{user.mention} successfully deleted from the database :white_check_mark:**")

bot.run(os.environ["token"])

