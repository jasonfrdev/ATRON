import discord
from discord.ext import commands
import logging
import random
import datetime
import settings
import requests
import youtube_dl

logger = logging.getLogger("bot")

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        someone = random.choice(ctx.guild.members)
        return f"{ctx.author} slaps {someone} with {argument}"

def get_bot_stats(bot):
    uptime = datetime.datetime.utcnow() - bot.start_time
    total_messages = sum(bot.messages_sent.values()) if hasattr(bot, 'messages_sent') else 0
    total_commands = len(bot.commands)
    
    
    total_servers = len(bot.guilds)
    total_members = sum(guild.member_count for guild in bot.guilds)
    avg_members_per_server = total_members / total_servers if total_servers else 0

    
    avg_messages_per_day = total_messages / (uptime.total_seconds() / 86400) if uptime.total_seconds() > 0 else 0
    
    
    active_voice_channels = sum(1 for guild in bot.guilds for channel in guild.voice_channels if channel.members)
    active_text_channels = sum(1 for guild in bot.guilds for channel in guild.text_channels if channel.members)
    

    return {
        "Total Servers": total_servers,
        "Total Members": total_members,
        "Avg. Members/Server": avg_members_per_server,
        "Avg. Messages/Day": avg_messages_per_day,
        "Active Voice Channels": active_voice_channels,
        "Active Text Channels": active_text_channels,
        
    }

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="+", intents=intents)

    @bot.event
    async def on_ready():
        bot.start_time = datetime.datetime.utcnow()
        bot.messages_sent = {}  # Hier könnten Nachrichtenstatistiken für verschiedene Server gespeichert werden
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    
    @bot.command(
        aliases=['p'],
        help="Help",
        description="See if the bot replies to your commands",
        brief="Ping the bot",
        enabled=True,
        hidden=False
    )
    async def ping(ctx):
        """ The bot answers with pong """
        await ctx.send("pong")
    
    @bot.command()    
    async def say(ctx, what="WHAT?"):
        await ctx.send(what)
    
    @bot.command()    
    async def say2(ctx, *what):
        await ctx.send(" ".join(what))
        
    @bot.command(
        aliases=['ch']
    )
    async def choices(ctx, *options):
        await ctx.send(random.choice(options))    
        
    @bot.command()    
    async def say3(ctx, what="WHAT?", why="WHY?"):
        await ctx.send(what + why)
        
    @bot.command()
    async def add(ctx, one: int, two: int):
        await ctx.send(one + two)
        
    @bot.command()
    async def joined(ctx, who: discord.Member):
        await ctx.send(who.joined_at)
        
    @bot.command()
    async def slap(ctx, reason: Slapper):
        await ctx.send(reason)
        
    @bot.event
    async def on_member_join(member):
        if member.guild.id == 1173273291750916147:
            role = member.guild.get_role(1173616327613751376)
            await member.add_roles(role)
        
    @bot.command(
        aliases=['sts']
        )
    async def stats(ctx):
        bot_stats = get_bot_stats(bot)
        
        embed = discord.Embed(title="Bot Statistics", color=0x7289DA)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")

        for stat, value in bot_stats.items():
            embed.add_field(name=stat, value=value, inline=False)

        await ctx.send(embed=embed)
        
    @bot.command()
    async def cat(ctx):
        response = requests.get('https://some-random-api.ml/img/cat')
        data = response.json()
        await ctx.send(data['link'])


    @bot.command()
    async def dog(ctx):
        response = requests.get('https://some-random-api.ml/img/dog')
        data = response.json()
        await ctx.send(data['link'])


    @bot.command()
    async def meme(ctx):
        response = requests.get('https://some-random-api.ml/meme')
        data = response.json()
        await ctx.send(data['image'])
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()