from discord.ext import commands


def get_all_emoji(client: commands.Bot):
    for server in client.guilds:
        print(f"{server.name} | {server.id}")
        for emoji in server.emojis:
            if emoji.animated:
                print(f"\t<a:{emoji.name}:{emoji.id}>")
            else:
                print(f"\t<:{emoji.name}:{emoji.id}>")
