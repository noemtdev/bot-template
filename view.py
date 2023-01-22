from discord.ui import View, button
import discord

class SuggestionView(View):
    def __init__(self, bot, message_id: int, voted: dict=None):
        super().__init__()

        self.timeout = None

        if voted is None:
            voted = {"up": [], "down": []}
            self.upvotes = 0
            self.downvotes = 0
            self.difference = 0
        else:
            self.upvotes = len(voted["up"])
            self.downvotes = len(voted["down"])
            self.difference = self.upvotes - self.downvotes

        self.voted: dict = voted
        self.message_id = message_id
        self.bot = bot

    async def edit_embed_color(self, message, embed, view, interaction):
        if self.difference < 0:
            embed.color = discord.Color.red()

        elif self.difference > 0:
            embed.color = discord.Color.green()

        else:
            embed.color = discord.Color.blurple()

        await message.edit(embed=embed, view=view)
        return await interaction.response.defer()

        


    @button(label="0", style=discord.ButtonStyle.blurple, emoji="👍", custom_id="upvote")
    async def upvote(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id in self.voted["up"]:

            self.upvotes -= 1
            self.difference -= 1

            self.voted["up"].remove(interaction.user.id)

            button.label = str(self.upvotes)
            self.children[1].label = str(self.difference)
            self.children[2].label = str(self.downvotes)

            if self.difference < 0:
                button.style = discord.ButtonStyle.red
                self.children[2].style = discord.ButtonStyle.green

            elif self.difference > 0:
                button.style = discord.ButtonStyle.green
                self.children[2].style = discord.ButtonStyle.red

            else:
                button.style = discord.ButtonStyle.blurple
                self.children[2].style = discord.ButtonStyle.blurple
        
        elif interaction.user.id in self.voted["down"]:
            self.downvotes -= 1
            self.difference += 2
            self.upvotes += 1

            self.voted["down"].remove(interaction.user.id)
            self.voted["up"].append(interaction.user.id)

            button.label = str(self.upvotes)
            self.children[1].label = str(self.difference)
            self.children[2].label = str(self.downvotes)

            if self.difference < 0:
                button.style = discord.ButtonStyle.red
                self.children[2].style = discord.ButtonStyle.green

            elif self.difference > 0:
                button.style = discord.ButtonStyle.green
                self.children[2].style = discord.ButtonStyle.red

            else:
                button.style = discord.ButtonStyle.blurple
                self.children[2].style = discord.ButtonStyle.blurple

        else:
            self.upvotes += 1
            self.difference += 1

            self.voted["up"].append(interaction.user.id)

            button.label = str(self.upvotes)
            self.children[1].label = str(self.difference)
            self.children[2].label = str(self.downvotes)

            if self.difference < 0:
                button.style = discord.ButtonStyle.red
                self.children[2].style = discord.ButtonStyle.green

            elif self.difference > 0:
                button.style = discord.ButtonStyle.green
                self.children[2].style = discord.ButtonStyle.red

            else:
                button.style = discord.ButtonStyle.blurple
                self.children[2].style = discord.ButtonStyle.blurple

        await self.edit_embed_color(interaction.message, interaction.message.embeds[0], self, interaction)

        await self.bot.suggestion_database.execute("UPDATE views SET voted = ? WHERE message_id = ?", (str(self.voted), self.message_id))
        await self.bot.suggestion_database.commit()

    @button(label="0", style=discord.ButtonStyle.blurple, disabled=True, custom_id="diff")
    async def diff(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @button(label="0", style=discord.ButtonStyle.blurple, emoji="👎", custom_id="downvote")
    async def downvote(self, button: discord.ui.Button, interaction: discord.Interaction):

        if interaction.user.id in self.voted["down"]:

            self.downvotes -= 1
            self.difference += 1

            self.voted["down"].remove(interaction.user.id)

            button.label = str(self.downvotes)
            self.children[1].label = str(self.difference)
            self.children[0].label = str(self.upvotes)

            if self.difference < 0:
                button.style = discord.ButtonStyle.red
                self.children[0].style = discord.ButtonStyle.green

            elif self.difference > 0:
                button.style = discord.ButtonStyle.green
                self.children[0].style = discord.ButtonStyle.red

            else:
                button.style = discord.ButtonStyle.blurple
                self.children[0].style = discord.ButtonStyle.blurple

        elif interaction.user.id in self.voted["up"]:
            self.upvotes -= 1
            self.difference -= 2
            self.downvotes += 1

            self.voted["up"].remove(interaction.user.id)
            self.voted["down"].append(interaction.user.id)

            self.children[1].label = str(self.difference)
            self.children[0].label = str(self.upvotes)

            button.label = str(self.downvotes)

            if self.difference < 0:
                button.style = discord.ButtonStyle.green
                self.children[0].style = discord.ButtonStyle.red

            elif self.difference > 0:
                button.style = discord.ButtonStyle.red
                self.children[0].style = discord.ButtonStyle.green

            else:
                button.style = discord.ButtonStyle.blurple
                self.children[0].style = discord.ButtonStyle.blurple

        else:
            self.downvotes += 1
            self.difference -= 1

            self.voted["down"].append(interaction.user.id)

            button.label = str(self.downvotes)
            self.children[1].label = str(self.difference)
            self.children[0].label = str(self.upvotes)

            if self.difference < 0:
                button.style = discord.ButtonStyle.green
                self.children[0].style = discord.ButtonStyle.red

            elif self.difference > 0:
                button.style = discord.ButtonStyle.red
                self.children[0].style = discord.ButtonStyle.green

            else:
                button.style = discord.ButtonStyle.blurple
                self.children[0].style = discord.ButtonStyle.blurple


        await self.edit_embed_color(interaction.message, interaction.message.embeds[0], self, interaction)

        await self.bot.suggestion_database.execute("UPDATE views SET voted = ? WHERE message_id = ?", (str(self.voted), self.message_id))
        await self.bot.suggestion_database.commit()
