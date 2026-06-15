

import discord

class Embeds:
    def the_hunt_winners():
        embed = discord.Embed(title="The Hunt Winners",
                            colour=0xfe86e4)

        embed.add_field(name="<:huberte:1514809555152932864> Chapter I (Hueycoatl)",
                        value="N/A\n",
                        inline=False)
        embed.add_field(name="<:ancient_hilt:1514809924515790889> Chapter II (Nex)",
                        value="<:1stplace:1514784685295927435> We Can Spoon, Voteyes2pvp\n",
                        inline=False)
        embed.add_field(name="<:warrior_helm:1514809925090545674> Chapter III (Barbarian Assault)",
                        value="<:1stplace:1514784685295927435> w1zzy, SithLordMeow, dnd5, ZaryteKnight, Pattaya\n",
                        inline=False)
        embed.add_field(name="<:ghrazi_rapier:1514810083278852126> Chapter IV (Theatre of Blood)",
                        value="(Ongoing)",
                        inline=False)

        embed.set_thumbnail(url="https://i.imgur.com/8GI8n4g.png")

        return embed
    
    def highest_kcs():
        embed = discord.Embed(title="Highest KCs",
                            colour=0xfe86e4)
        return embed