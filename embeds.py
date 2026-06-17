

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
    
    def highest_kcs(data, category_name):
        embed = discord.Embed(title=category_name,
                            colour=0xfe86e4)
        
        for key in data:
            print("Generating", key)
            embed.add_field(name=get_clean_name(key), value=f"> {data[key]['normie']['name']} - {data[key]['normie']['kills']} KC\n> <:ironman:1516279477657800724> {data[key]['iron']['name']} - {data[key]['iron']['kills']} KC", inline = False)

        return embed
    
def get_clean_name(boss_name: str):
    clean_names = {
        "commander_zilyana": "Commander Zilyana",
        "general_graardor": "General Graardor",
        "kril_tsutsaroth": "K'ril Tsutsaroth",
        "kreearra": "Kree'arra",
        "nex": "Nex",
        "chambers_of_xeric": "Chambers of Xeric",
        "chambers_of_xeric_challenge_mode": "Chambers of Xeric: CM",
        "theatre_of_blood": "Theatre of Blood",
        "theatre_of_blood_hard_mode": "Theatre of Blood: HM",
        "tombs_of_amascut": "Tombs of Amascut",
        "tombs_of_amascut_expert": "Tombs of Amascut: XM"
    }
    return clean_names[boss_name]