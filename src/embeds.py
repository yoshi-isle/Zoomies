import discord


class Embeds:
    def the_hunt_winners():
        embed = discord.Embed(title="The Hunt Winners", colour=0xFE86E4)

        embed.add_field(
            name="<:huberte:1514809555152932864> Chapter I (Hueycoatl)",
            value="N/A\n",
            inline=False,
        )
        embed.add_field(
            name="<:ancient_hilt:1514809924515790889> Chapter II (Nex)",
            value="<:1stplace:1514784685295927435> We Can Spoon, Voteyes2pvp\n",
            inline=False,
        )
        embed.add_field(
            name="<:warrior_helm:1514809925090545674> Chapter III (Barbarian Assault)",
            value="<:1stplace:1514784685295927435> w1zzy, SithLordMeow, dnd5, ZaryteKnight, Pattaya\n",
            inline=False,
        )
        embed.add_field(
            name="<:ghrazi_rapier:1514810083278852126> Chapter IV (Theatre of Blood)",
            value="N/A\n",
            inline=False,
        )

        embed.set_thumbnail(url="https://i.imgur.com/8GI8n4g.png")

        return embed

    def highest_kcs(data, category_name):
        embed = discord.Embed(title=category_name, colour=0xFE86E4)

        for key in data:
            # convert to comma format 1234 = 1,234
            player_normie = data[key]['normie']['name']
            player_iron = data[key]['iron']['name']
            metric_normie = data[key]['normie']['kills']
            metric_iron = data[key]['iron']['kills']
            terminology = data[key]['normie']['terminology']

            embed.add_field(
                name=get_clean_name(key),
                value=f"> {player_normie} - {metric_normie:,} {terminology}\n> <:ironman:1516279477657800724> {player_iron} - {metric_iron:,} {terminology}",
                inline=False,
            )

        return embed


def get_clean_name(boss_name) -> str:
    clean_name = str(boss_name.name)
    # Add a space between each uppercase letter
    for i in range(len(clean_name) - 1, 0, -1):
        if clean_name[i].isupper() and clean_name[i - 1].islower():
            clean_name = clean_name[:i] + " " + clean_name[i:]

    return clean_name
