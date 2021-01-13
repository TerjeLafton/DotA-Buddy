import os
import asyncio

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="!")


class BotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = None
        self.clock_running = False
        self.minutes = 0
        self.seconds = 0
        self.last_event = "Match started!"

        self.clock.start()

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(675662039942955019)
        self.voice = await channel.connect()
        print(f"{self.bot.user.name} has successfully connected to the Discord server!")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(user).split("#")[0] != self.bot.user.name:
            if reaction.message.id == self.message.id:
                if reaction.emoji == "✅":
                    self.clock_running = True
                elif reaction.emoji == "❎":
                    self.clock_running = False
                elif reaction.emoji == "⏮":
                    self.seconds -= 10
                elif reaction.emoji == "⏪":
                    self.seconds -= 1
                elif reaction.emoji == "⏩":
                    self.seconds += 1
                elif reaction.emoji == "⏭":
                    self.seconds += 10

    @commands.command(name="time")
    async def time(self, ctx):
        self.message = await ctx.send(
            f"```Match has not started yet!\n\n" f"Click the ✅ to start the match!```"
        )
        await self.message.add_reaction("✅")
        await self.message.add_reaction("❎")
        await self.message.add_reaction("⏮")
        await self.message.add_reaction("⏪")
        await self.message.add_reaction("⏩")
        await self.message.add_reaction("⏭")

    @tasks.loop(seconds=1)
    async def clock(self):
        print(self.seconds)
        if self.message:
            if self.clock_running:
                if self.minutes % 5 == 4 and self.seconds == 45:
                    self.voice.play(discord.FFmpegPCMAudio('runes.mp3'))
                    self.last_event = (
                        f"{self.minutes}:{self.seconds}: Bounty rune in 15 seconds!"
                    )

                if self.seconds >= 59:
                    self.seconds = 0
                    self.minutes += 1
                else:
                    self.seconds += 1

            await self.message.edit(
                content=f"```Match has started!\n\n"
                f"Time: {self.minutes}:{self.seconds}\n\n"
                f"Last event -  {self.last_event}```"
            )


client.add_cog(BotCog(client))
client.run(TOKEN)
