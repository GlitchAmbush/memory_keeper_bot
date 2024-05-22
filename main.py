# main.py

# BOT MAIN
import os
import discord
import time
import logging_calculator as calc
import re
import traceback

from datetime import datetime
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands, tasks

# LOAD TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = commands.Bot(command_prefix="$", help_command=None, intents=intents)

# MESSAGE FUNCTION
async def on_message(message: Message) -> None:
    member=message.author
    
    # Ignore bots
    if member.bot==False:
        # debug log
        t0=time.time()
        print(f"[33m<{time.strftime('%d. %m. %H:%M:%S', time.localtime())} | Message in [0m{message.channel} [33mby [0m{message.author}[33m>[0m\n{message.content[:100]}")
        
        await client.process_commands(message)
        
        # more debug
        print(f" - processing time: {time.time()-t0}")

# HANDLE EVENTS
@client.event
async def on_ready() -> None:
    activity = discord.CustomActivity("Weaving fate... | $help")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f'{client.user} has connected to Discord!')

# COMMANDS
# $ping
@client.command()
async def ping(ctx: commands.Context) -> None: 
    await ctx.send(f'Pong;\n{client.latency * 1000}ms')
    # Expected: Pong: <val>ms

# $help
@client.command()
async def help(ctx: commands.Context, *args) -> None:
    p: str = client.command_prefix
    tembed: str = discord.Embed(title='The Memory Keeper aids you...', color=ctx.author.color)
    tembed.set_thumbnail(url='https://img3.gelbooru.com//samples/75/c6/sample_75c6ad9c9356da542e90ee153acff65f.jpg')
    tembed.add_field(name='Main Commands',
                    value=f'''`{p}log <start link> <end link> <levels>` - Calculate and log RP rewards and time
`{p}ping` - Returns ping (ms)''',
                    inline=False)
    tembed.add_field(name='More Help',
                    value=f'`{p}help <command>` - Gives more info on a command',
                    inline=False)

    if len(args) == 1:
        if args[0] == 'log':
            tembed: str = discord.Embed(title='The Memory Keeper aids you...', 
                                    description=f'''`{p}log <start link> <end link> <levels>`\n
**IMPORTANT!!** `<start link>` and `<end link>` __DO NOT__ count towards rewards.\n
The `<levels>` argument must be replaced with the levels of the characters involved in the RP. For example:
> `{p}log <start link> <end link> 13 14` is used to log levels 13 and 14.''', 
                                    color=ctx.author.color)
            tembed.set_thumbnail(url='https://img3.gelbooru.com//samples/75/c6/sample_75c6ad9c9356da542e90ee153acff65f.jpg')
    
    await ctx.send(embed=tembed)

# $log
@client.command()
async def log(ctx: commands.Context, message_start: discord.PartialMessage = '', message_end: discord.PartialMessage = '', *args) -> None:
    regxp = re.compile(r'^> ')
    
    if message_start == '' or message_end == '':
        tembed: str = discord.Embed(title="[ERROR]",
                                description=f'Command missing `<start link>` OR `<end link>`',
                                color=ctx.author.color)
        tembed.set_thumbnail(url='https://img3.gelbooru.com//samples/75/c6/sample_75c6ad9c9356da542e90ee153acff65f.jpg')
    else: 
        channel = message_start.channel

    # Check if args has input
    if args:
        # Message info list
        msg_info: list = []
        async for message in channel.history(limit=None, after=message_start, before=message_end):
            if message.author.bot and not message.author.id == 261302296103747584:
                msg_info.append(message)

        # Gets Messages
        messages: list = []
        for msg in msg_info:
            messages.append(msg.content)
        # print(messages)

        # Gets lines, removing Tupper Reply Quotes
        lines: list = []
        for line in messages:
            new_line = line.split('\n')
            if regxp.search(new_line[0]):
                # print("MATCH FOUND")
                for i in range(2):
                    new_line.pop(0)
            # else:
            #     print("MATCH NOT FOUND")
            
            for n in new_line:
                lines.append(n)
        # print('\nNew Lines: ', lines)
        
        # Gets words
        words: list = []
        for line in lines:
            for t in line.split():
                new_text = re.sub(r"[^a-zA-Z0-9 ]", "", t)
                words.append(new_text)
        # print('\nWords: ', words)
        
        # Changes args (str) into int
        levels: list[int] = []
        for level in args:
            levels.append(int(level))

        # Embed
        tembed: str = discord.Embed(title='Another Memory Kept...', description=f'{calc.print_rewards_info(levels, words)}', color=ctx.author.color)
        tembed.set_thumbnail(url='https://img3.gelbooru.com//samples/75/c6/sample_75c6ad9c9356da542e90ee153acff65f.jpg')
        tembed.add_field(name='RP Start', value=f'{message_start.jump_url}', inline=False)
        tembed.add_field(name='RP End', value=f'{message_end.jump_url}', inline=False)
    else:
        # Default
        tembed: str = discord.Embed(title="$log Command",
                                description=f'''`log <start link> <end link> <levels>`\n
**IMPORTANT!!** `<start link>` and `<end link>` __DO NOT__ count towards rewards.\n
The `<levels>` argument must be replaced with the levels of the characters involved in the RP. For example:
> `log <start link> <end link> 13 14` is used to log levels 13 and 14.''',
                                color=ctx.author.color)
        tembed.set_thumbnail(url='https://img3.gelbooru.com//samples/75/c6/sample_75c6ad9c9356da542e90ee153acff65f.jpg')
    
    await ctx.message.delete()
    await ctx.send(embed=tembed)



# $test
@client.command()
async def test(ctx: commands.Context, message_start: discord.PartialMessage, message_end: discord.PartialMessage, *args) -> None:
    cregxp = re.compile(r'^> ')
    pause_duration = 3600
    
    if message_start == '' or message_end == '':
        tembed: str = discord.Embed(title="[ERROR]",
                                description=f'Command missing `<start link>` OR `<end link>`',
                                color=ctx.author.color)
        tembed.set_thumbnail(url='https://img3.gelbooru.com//samples/75/c6/sample_75c6ad9c9356da542e90ee153acff65f.jpg')
    else: 
        channel = message_start.channel

        # Message info list
        msg_info: list = []
        async for message in channel.history(limit=None, after=message_start, before=message_end):
            if message.author.bot and not message.author.id == 261302296103747584:
                msg_info.append(message)

        # Gets Messages
        messages: list = []
        for msg in msg_info:
            messages.append(msg.content)
        # print(messages)

        # Gets lines, removing Tupper Reply Quotes
        lines: list = []
        for line in messages:
            new_line = line.split('\n')
            if cregxp.search(new_line[0]):
                # print("MATCH FOUND")
                for i in range(2):
                    new_line.pop(0)
            # else:
            #     print("MATCH NOT FOUND")
            
            for n in new_line:
                lines.append(n)
        # print('\nNew Lines: ', lines)
        
        # Gets content -> gets words w/o special characters and punctuation
        rp_duration = 0
        timestamps: list[int] = []
        words: list[str] = []
        for msg in messages:
            for t in msg.content.split():
                new_text = re.sub(r"[^a-zA-Z0-9 ]", "", t)
                words.append(new_text)
            msg_timestamp = ((int(msg.id) >> 22) + 1420070400000) // 1000
            if not timestamps:
                pass
            else:
                delta = msg_timestamp - timestamps[-1]
                rp_duration += min(delta, pause_duration)
            timestamps.append(msg_timestamp)
        
        # Changes args (str) into int
        levels: list[int] = []
        for level in args:
            levels.append(int(level))

        # Embed
        tembed: str = discord.Embed(title='Another Memory Kept...', description=f'{calc.print_rewards_info(levels, words)}', color=ctx.author.color)
        tembed.set_thumbnail(url='https://img3.gelbooru.com//samples/75/c6/sample_75c6ad9c9356da542e90ee153acff65f.jpg')
        tembed.add_field(name='RP Start', value=f'{message_start.jump_url}', inline=False)
        tembed.add_field(name='RP End', value=f'{message_end.jump_url}', inline=False)

    await ctx.send(content="Command recieved...")
    await ctx.send(content="Testing...")
    await ctx.send(content="COMPLETE. Data sent to terminal.")

    await ctx.send(embed=tembed)



# MAIN ENTRY
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()