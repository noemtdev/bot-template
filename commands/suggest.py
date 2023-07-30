import discord
from discord import Option
from discord.ext import commands
from view import SuggestionView
import datetime


class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="suggest",
        description="Suggests Something",
    )
    async def suggest(self, ctx, suggestion: Option(str, "Expain your suggestion as well as possible.", required=True)):

        embed = discord.Embed(
            title=f"Suggestion by {ctx.author.name}",
            description=suggestion,
            color=discord.Color.blurple()
        )
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
    
        ms = await self.bot.get_channel(self.bot.suggestions_channel).send(embed=embed)
        await ms.edit(view=SuggestionView(self.bot, message_id=ms.id))

        await self.bot.suggestion_database.execute("INSERT INTO views (message_id, voted) VALUES (?, ?)", (ms.id, str({"up": [], "down": []})))
        await self.bot.suggestion_database.commit()

        return await ctx.respond("Your suggestion has been sent!", ephemeral=True)

def setup(bot):
    bot.add_cog(Suggest(bot))
