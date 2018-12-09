from redbot.core import commands
import discord
import requests
import random


class Overwatch(commands.Cog):
    """SA:MP Related Commands"""

    @commands.group(autohelp=True)
    async def ow(self, ctx):
        """OW Commands"""
        pass

    @ow.command()
    async def profile(self, ctx, account: str, region: str, platform=None):
        """OW Profile Stats - Account must include the ID. Ensure profile is public for full stats"""
        account = account.replace("#", "-")
        if platform != "psn" or platform != "xbl":
            platform = "pc"
        try:
            r = requests.get(
                f"https://ow-api.com/v1/stats/{platform}/{region}/{account}/profile")
            colour = discord.Color.from_hsv(random.random(), 1, 1)
            embed = discord.Embed(title="Overwatch Profile Information", colour=colour)
            embed.set_author(name=r.json()['name'], icon_url=r.json()['icon'])
            embed.set_thumbnail(url=r.json()['icon'])
            embed.add_field(name="Name:", value=r.json()['name'], inline=True)
            embed.add_field(name="Level:", value=r.json()['level'], inline=True)
            embed.add_field(name="Prestige:", value=r.json()['prestige'], inline=True)
            if r.json()['private'] == False:
                embed.add_field(name="Games Won:", value=r.json()['gamesWon'], inline=True)
            else:
                embed.set_footer(text="Please set your profile status to public for more stats.")
            await ctx.send(embed=embed)
        except:
            await ctx.send("Request failed, please ensure you're entering the details correctly.")

    @ow.command()
    async def heroes(self, ctx, account: str, region: str, hero: str, platform=None):
        """OW Hero Stats - Account must include the ID. Profile must be public"""
        account = account.replace("#", "-")
        if platform != "psn" or platform != "xbl":
            platform = "pc"
        try:
            r = requests.get(
                f"https://ow-api.com/v1/stats/{platform}/{region}/{account}/heroes/{hero}")
            if r.json()['private'] == False:
                colour = discord.Color.from_hsv(random.random(), 1, 1)
                embed = discord.Embed(title="Overwatch Profile Information", colour=colour)
                embed.set_author(name=r.json()['name'], icon_url=r.json()['icon'])
                embed.set_thumbnail(url=r.json()['icon'])
                embed.add_field(name="Name:", value=r.json()['name'], inline=True)
                embed.add_field(name="Level:", value=r.json()['level'], inline=True)
                embed.add_field(name="Prestige:", value=r.json()['prestige'], inline=True)
                embed.add_field(name="Total Games Won:", value=r.json()['gamesWon'], inline=True)
                embed.add_field(name="---", value="---", inline=False)
                embed.add_field(name="Hero:", value=hero.capitalize(), inline=True)
                embed.add_field(name=hero.capitalize() + " Playtime:",
                                value=r.json()['quickPlayStats']['topHeroes']['{}'.format(hero)]['timePlayed'],
                                inline=True)
                embed.add_field(name="Games Won:",
                                value=r.json()['quickPlayStats']['topHeroes']['{}'.format(hero)]['gamesWon'],
                                inline=True)
                embed.add_field(name="Elims Per Life",
                                value=r.json()['quickPlayStats']['topHeroes']['{}'.format(hero)][
                                    'eliminationsPerLife'],
                                inline=True)
                embed.add_field(name="Weapon Accuracy",
                                value=r.json()['quickPlayStats']['topHeroes']['{}'.format(hero)]['weaponAccuracy'],
                                inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Your profile is set to private, we were unable to retrieve your stats.")

        except:
            await ctx.send("Request failed, please ensure you're entering the details correctly.")
