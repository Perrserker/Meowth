from discord.ext import commands

class BotCommand:
    """Convert string to Command object from Bot.

    Returns
    --------
    :class:`discord.ext.commands.Command`
    """
    @classmethod
    async def convert(cls, ctx, arg):
        cmd = ctx.bot.get_command(arg)
        if cmd is None:
            raise commands.BadArgument(f"Command not found.")
        return cmd

class Multi(commands.Converter):
    """Convert multiple conversion types.

    Conversion will be attempted in order of first type to last type.

    Parameters
    -----------
    *types
        Types to be attempted for arg conversion
    """
    def __init__(self, *types):
        self.types = types

    async def convert(self, ctx, arg):
        for type_ in self.types:
            try:
                return await ctx.command.do_conversion(ctx, type_, arg)
            except Exception as e:
                continue
        type_names = ', '.join([t.__name__ for t in self.types])
        raise commands.BadArgument(
            f"{arg} was not able to convert to the following types: "
            f"{type_names}")

class Guild:
    """Convert Guild object by ID or name.

    Returns
    --------
    :class:`discord.Guild`
    """
    @classmethod
    async def convert(cls, ctx, arg):
        guild = None
        if arg.isdigit():
            guild = ctx.bot.get_guild(int(arg))
        if not guild:
            guild = ctx.bot.find_guild(arg)
        return guild


class ChannelMessage:
    """Get tuple of Channel and Message objects from string of format '{channelid}/{messageid}'.

    Returns
    --------
    :class:`tuple(discord.Channel, discord.Message)`
    """
    @classmethod
    async def from_id_string(cls, bot, arg: str):
        ids = arg.split('/')
        channelid = int(ids[0])
        messageid = int(ids[1])
        channel = bot.get_channel(channelid)
        if not channel:
            return None, None
        try:    
            message = await channel.fetch_message(messageid)
        except:
            return channel, None
        return (channel, message)


