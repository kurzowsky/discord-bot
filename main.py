from typing import Final
from dotenv import load_dotenv
import os
import discord
from discord import Intents, Message, Member
from discord.ext import commands
import nest_asyncio
import json
from responses import get_faceit_stats

nest_asyncio.apply()
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def faceit(ctx, *, profile_url: str):
    """Wpisz !faceit <link do profilu FACEIT>, aby sprawdzić statystyki."""
    try:
        # Wydobywanie nicku z linku
        if "faceit.com" in profile_url or "faceittracker.net" in profile_url:
            player_name = profile_url.split("/")[-1]
        else:
            await ctx.send("Podano nieprawidłowy link. Użyj formatu: https://faceittracker.net/players/NICKNAME")
            return

        # Pobieranie statystyk
        stats = get_faceit_stats(player_name)
        print(stats)
        if not stats:
            await ctx.send("Nie udało się pobrać statystyk dla tego gracza. Sprawdź, czy nick jest poprawny.")
            return

        # Tworzenie odpowiedzi
        embed = discord.Embed(title=f"**Statystyki FACEIT dla {player_name}**", color=0x00ff00)
        embed.add_field(name="Poziom", value=stats["level"], inline=True)
        embed.add_field(name="ELO", value=stats["elo"], inline=True)
        embed.add_field(name="Rozegrane mecze", value=stats["matches"], inline=True)
        embed.add_field(name="Win Rate", value=f"{stats['winrate']}", inline=True)
        embed.add_field(name="Headshot Rate", value=f"{stats['headshots']}", inline=True)
        embed.add_field(name="K/D Ratio", value=f"{stats['kd_ratio']}", inline=True)
        embed.add_field(name="**LAST 10 MATCHES**", value="", inline=False)
        embed.add_field(name="K/D Ratio", value=f"{stats['k/d_ratio_last_10']}", inline=True)
        embed.add_field(name="Wins", value=f"{stats['wins']}", inline=True)
        embed.add_field(name="Losses", value=f"{stats['losses']}", inline=True)
        embed.add_field(name="Results", value=f"{stats['last_10_results']}", inline=True)

        embed.set_footer(text="Statystyki dostarczone przez FaceitTracker.net")

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("Wystąpił błąd podczas przetwarzania żądania.")
        print(e)

@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is on')
    activity = discord.CustomActivity(name='Owner: kurzowskyy')
    await bot.change_presence(activity=activity)
    channel = bot.get_channel(1244337321608876042)
    channel2 = bot.get_channel(941297332631261216)
    if channel:
        await channel.send('Jestem online')
        #await channel2.send('popiel to cwel123')
    else:
        print('Brak kanału')

file = open("lista", "r")
user_list = []
for line in file:
    line = line.strip()
    user_list.append(line)
print(user_list)

@bot.event
async def on_presence_update(before: Member, after: Member):
    if before.status == discord.Status.offline and after.status != discord.Status.offline:
        channel = after.guild.get_channel(1244337321608876042)
        if after.display_name == 'kurzowskyy':
            kurzowskyy = discord.utils.get(after.guild.members, display_name='kurzowskyy')
            if kurzowskyy:
                try:
                    await kurzowskyy.send(f'{after.display_name} jest teraz online!')
                except Exception as e:
                    print(f'Nie udało się wysłać wiadomości prywatnej: {e}')
        if channel:
            #if after.display_name in user_list:
            await channel.send(f'{after.display_name} jest teraz online!')

@bot.command(name='zmien_nick')
@commands.has_permissions(manage_nicknames=True)
async def change_nick(ctx, member: Member, *, new_nickname: str):
    try:
        old_nickname = member.display_name
        await member.edit(nick=new_nickname)
        await ctx.send(f'Pseudonim użytkownika {old_nickname} został zmieniony na {new_nickname}')
    except discord.Forbidden:
        await ctx.send('Nie mam uprawnień do zmiany pseudonimu tego użytkownika.')
    except discord.HTTPException as e:
        await ctx.send(f'Wystąpił błąd podczas zmiany pseudonimu: {e}')

#1162071933991538740
#484318765954105344
@bot.event
async def on_member_update(before: Member, after: Member) -> None:
    if after.id == 484318765954105344 and before.nick != after.nick:
        new_nick = f"pantoflarz"

        try:
            await after.edit(nick=new_nick)
            print(f'Zmieniono pseudonim użytkownika {after.display_name} na {new_nick}')
        except discord.Forbidden:
            print(f'Bot nie ma uprawnień do zmiany pseudonimu użytkownika {after.display_name}')
        except discord.HTTPException as e:
            print(f'Wystąpił błąd podczas zmiany pseudonimu użytkownika {after.display_name}: {e}')

def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
