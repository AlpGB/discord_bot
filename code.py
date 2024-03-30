import discord
from discord.ext import commands
import random
import socket
import aiohttp
import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

facts = [
    "Did you know that the shortest war in history lasted only 38 minutes? It was between Britain and Zanzibar in 1896.",
    "The world's oldest piece of chewing gum is over 9,000 years old!",
    "A bolt of lightning is six times hotter than the sun.",
    "The average person spends six months of their life waiting for a red light to turn green.",
    "Bananas are berries, but strawberries aren't.",
    "An ostrich's eye is bigger than its brain.",
    "The dot over the letter 'i' is called a tittle.",
    "There are more possible iterations of a game of chess than there are atoms in the known universe.",
    "Honey never spoils.",
    "The longest English word is 189,819 letters long.",
    "The longest wedding veil was longer than 63 football fields.",
    "A hummingbird weighs less than a penny."
]

jokes = [
    "Why don't scientists trust atoms?\nBecause they make up everything!",
    "Parallel lines have so much in common.\nIt's a shame they'll never meet.",
    "I'm reading a book on anti-gravity.\nIt's impossible to put down!",
    "I told my wife she was drawing her eyebrows too high.\nShe looked surprised.",
    "Why don't skeletons fight each other?\nThey don't have the guts.",
    "Why couldn't the bicycle stand up by itself?\nIt was two-tired.",
    "Why did the scarecrow win an award?\nBecause he was outstanding in his field."
]

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')

@bot.command()
async def commands(ctx):
    if any(role.name == 'MOD' for role in ctx.author.roles):
        await ctx.send('List of available commands:\n'
                       '   !ping - Check bot latency\n'
                       '   !userinfo [user] - Get user information\n'
                       '   !kick [user] - Kick user from the server\n'
                       '   !ban [user] - Ban user from the server\n'
                       '   !mute [user] - Mute user in text channels\n'
                       '   !unmute [user] - Unmute previously muted user\n'
                       '   !multi_delete [number] - deletes a certain amount of numbers\n'
                       '   !joke - Tell a joke\n'
                       '   !fact - Share an interesting fact\n'
                       '   !gif - Get a random gif\n'
                       '   !roll [dice] - Roll dice (e.g., !roll 2d6)\n'
                       '   !rps [choice] - Play rock-paper-scissors against the bot\n'
                       '   !serverinfo - Get information about the current server\n'
                       '   !multi_kick [number of kicks] - Kicks multiple people\n'
                       '   !multi_ban [number of bans] - Bans multiple people\n'
                       '   !channelinfo [channel] - Get information about a specific channel\n'
                       '   !countdown [date] - Create a countdown to a specific date\n'
                       '   !calculate [expression] - Perform a calculation\n')
    else:
        await ctx.send('List of available commands:\n'
                       '   !ping - Check bot latency\n'
                       '   !userinfo [user] - Get user information\n'
                       '   !joke - Tell a joke\n'
                       '   !gif - Get a random gif\n'
                       '   !roll [dice] - Roll dice (e.g., !roll 2d6)'
                       '   !rps [choice] - Play rock-paper-scissors against the bot\n'
                       '   !serverinfo - Get information about the current server\n'
                       '   !channelinfo [channel] - Get information about a specific channel\n'
                       '   !countdown [date] - Create a countdown to a specific date\n'
                       '   !calculate [expression] - Perform a calculation\n')

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')

@bot.command()
async def userinfo(ctx, member: discord.Member):
    if discord.utils.get(ctx.author.roles, name='MOD'):
        try:
            ip_address = socket.gethostbyname(member.name)
            await ctx.send(f'User: {member.name}\n'
                           f'ID: {member.id}\n'
                           f'Created at: {member.created_at}\n'
                           f"IP address: {ip_address}")
        except socket.gaierror:
            await ctx.send(f'User: {member.name}\n'
                           f'ID: {member.id}\n'
                           f'Created at: {member.created_at}\n'
                           f"IP address: unable to retrieve ip")

@bot.command()
async def kick(ctx, member: discord.Member):
    if discord.utils.get(ctx.author.roles, name='MOD'):
        await member.kick()
        await ctx.send(f'{member.mention} has been kicked from the server.')

@bot.command()
async def ban(ctx, member: discord.Member):
    if discord.utils.get(ctx.author.roles, name='MOD'):
        await member.ban()
        await ctx.send(f'{member.mention} has been banned from the server.')

@bot.command()
async def mute(ctx, member: discord.Member):
    if discord.utils.get(ctx.author.roles, name='MOD'):
        role = discord.utils.get(ctx.guild.roles, name="kurt_kole")
        await member.add_roles(role)
        await ctx.send(f'{member.mention} has been muted.')

@bot.command()
async def unmute(ctx, member: discord.Member):
    if discord.utils.get(ctx.author.roles, name='MOD'):
        role = discord.utils.get(ctx.guild.roles, name="kürt_köle")
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} has been unmuted.')

@bot.command()
async def fact(ctx):
    random_fact = random.choice(facts)
    await ctx.send(random_fact)

@bot.command()
async def joke(ctx):
    random_joke = random.choice(jokes)
    await ctx.send(random_joke)

@bot.command()
async def gif(ctx):
    # You can implement the logic to fetch a random gif here
    await ctx.send("Here's a random gif: https://giphy.com/random")

@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(result)

@bot.command()
async def multi_delete(ctx, number: int):
    if number > 100:
        await ctx.send('The messages you delete at once cannot be bigger than 100')
    else:
        messages = []
        async for message in ctx.channel.history(limit=number + 1):
            messages.append(message)
        for message in messages:
            await message.delete()
            
@bot.command()
async def serverinfo(ctx):
    # Implement logic to retrieve and display server info
    await ctx.send("Server Information:\nName: {}\nOwner: {}\nRegion: {}".format(ctx.guild.name, ctx.guild.owner, ctx.guild.region))

@bot.command()
async def rps(ctx, choice: str):
    # Implement logic to play rock-paper-scissors
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)
    await ctx.send(f"Bot chose: {bot_choice}")
    if choice.lower() in choices:
        if choice.lower() == bot_choice:
            await ctx.send("It's a tie!")
        elif (choice.lower() == "rock" and bot_choice == "scissors") or \
             (choice.lower() == "paper" and bot_choice == "rock") or \
             (choice.lower() == "scissors" and bot_choice == "paper"):
            await ctx.send("You win!")
        else:
            await ctx.send("Bot wins!")
    else:
        await ctx.send("Invalid choice. Please choose 'rock', 'paper', or 'scissors'.")

@bot.command()
async def channelinfo(ctx, channel: discord.TextChannel):
    # Implement logic to retrieve and display channel info
    await ctx.send(f"Channel Information:\nName: {channel.name}\nID: {channel.id}\nCategory: {channel.category}\nTopic: {channel.topic}")

@bot.command()
async def multi_kick(ctx, number: int):
    if number <= 0:
        await ctx.send("Please provide a valid number of kicks.")
        return

    await ctx.send(f"Please type {number} user(s) to kick, one by one.")

    kicked_users = []
    for _ in range(number):
        try:
            message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
            if message.content.startswith('@'):
                member_name = message.content[1:].strip()
                member = discord.utils.get(ctx.guild.members, name=member_name)
                if member:
                    kicked_users.append(member)
                else:
                    await ctx.send(f"User {member_name} not found in the server.")
            else:
                await ctx.send("Please mention the user to kick using '@' followed by their username.")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to input the users. Command canceled.")
            return

    for user in kicked_users:
        try:
            await user.kick(reason="Multi-kick command by moderator.")
            await ctx.send(f"Kicked {user.mention}.")
        except discord.Forbidden:
            await ctx.send(f"Couldn't kick {user.name}. Missing permissions or higher role.")

@bot.command()
async def multi_ban(ctx, number: int):
    if number <= 0:
        await ctx.send("Please provide a valid number of bans.")
        return

    await ctx.send(f"Please type {number} user(s) to ban, one by one.")

    banned_users = []
    for _ in range(number):
        try:
            message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
            if message.content.startswith('@'):
                member_name = message.content[1:].strip()
                member = discord.utils.get(ctx.guild.members, name=member_name)
                if member:
                    banned_users.append(member)
                else:
                    await ctx.send(f"User {member_name} not found in the server.")
            else:
                await ctx.send("Please mention the user to ban using '@' followed by their username.")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to input the users. Command canceled.")
            return

    for user in banned_users:
        try:
            await ctx.guild.ban(user, reason="Multi-ban command by moderator.")
            await ctx.send(f"Banned {user.mention}.")
        except discord.Forbidden:
            await ctx.send(f"Couldn't ban {user.name}. Missing permissions or higher role.")

@bot.command()
async def countdown(ctx, date_str: str):
    try:
        target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        current_date = datetime.datetime.now()
        remaining_time = target_date - current_date
        await ctx.send(f"Countdown to {target_date.strftime('%Y-%m-%d %H:%M:%S')}:\n"
                       f"{remaining_time.days} days, {remaining_time.seconds // 3600} hours, "
                       f"{(remaining_time.seconds // 60) % 60} minutes, {remaining_time.seconds % 60} seconds left.")
    except ValueError:
        await ctx.send("Please provide a valid date in the format YYYY-MM-DD.")

@bot.command()
async def calculate(ctx, *, expression: str):
    try:
        result = eval(expression)
        await ctx.send(f"Result: {result}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def mem(ctx):
    with open('images/mem1.jpg', 'rb') as f:
        # Dönüştürülen Discord kütüphane dosyasını bu değişkende saklayalım!
        picture = discord.File(f)
   # Daha sonra bu dosyayı bir parametre olarak gönderebiliriz!
    await ctx.send(file=picture)

bot.run('BOT TOKEN HERE')
