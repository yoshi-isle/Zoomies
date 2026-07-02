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
            player_normie = data[key]["normie"]["name"]
            player_iron = data[key]["iron"]["name"]
            metric_normie = data[key]["normie"]["kills"]
            metric_iron = data[key]["iron"]["kills"]
            terminology = data[key]["normie"]["terminology"]

            embed.add_field(
                name=f"{get_clean_name(key)} {data[key]['emote']}",
                value=f"> {player_normie} - {metric_normie:,} {terminology}\n> <:ironman:1516279477657800724> {player_iron} - {metric_iron:,} {terminology}",
                inline=False,
            )

        embed.add_field(
            name="",
            value="Last updated: " + discord.utils.format_dt(discord.utils.utcnow()),
        )

        return embed

    def pb_category(display: dict):
        embed = discord.Embed(
            title="",
            timestamp=discord.utils.utcnow(),
        )

        embed.set_footer(text="")

        for activity_name, (submissions, emoji, amount_to_display) in display.items():
            value_lines = []

            trophy_emojis = {
                1: "<:1stplace:1514784685295927435>",
                2: "<:2ndplace:1514784692996669490>",
                3: "<:3rdplace:1514784698692276426>",
            }
            # Show existing submissions
            for i, sub in enumerate(submissions[:amount_to_display], 1):
                date_str = (
                    sub["create_time"].strftime("%Y-%m-%d")
                    if sub["create_time"]
                    else "-"
                )
                players = sub["players"] or "Unknown"
                metric = convert_game_ticks_to_time(sub["metric"])

                # trophy emoji
                line = f"> {trophy_emojis.get(i, '')} **{metric}** • {players} • {date_str}"

                if sub.get("imgur_url"):
                    line += " [(proof)](" + sub["imgur_url"] + ")"

                value_lines.append(line)

            # Fill remaining slots up to 3
            for i in range(len(submissions) + 1, amount_to_display + 1):
                value_lines.append(f"> {trophy_emojis.get(i, '')} -")

            embed.add_field(
                name=f"{activity_name} {emoji}",
                value="\n".join(value_lines),
                inline=False,
            )

        return embed

    def changelog(
        players: str,
        activity: str,
        metric: str,
        imgur_url: str,
        leaderboard_url: str,
        new_placement: int | None,
    ):
        embed = discord.Embed(
            title="New PB Achieved!",
            colour=0xFE86E4,
            timestamp=discord.utils.utcnow(),
        )

        embed.add_field(
            name="Submitter(s)",
            value=players,
        )

        embed.add_field(
            name="Activity",
            value=activity,
        )

        # TODO - Time or integer
        embed.add_field(
            name="PB",
            value=convert_game_ticks_to_time(metric),
        )

        embed.add_field(
            name="Ranking",
            value="<:1stplace:1514784685295927435> 1st place!"
            if new_placement == 1
            else "<:2ndplace:1514784692996669490> 2nd place"
            if new_placement == 2
            else "<:3rdplace:1514784698692276426> 3rd place",
        )

        embed.add_field(
            name="",
            value=f"Check out the leaderboard [here]({leaderboard_url})",
        )

        if imgur_url:
            embed.set_image(url=imgur_url)

        return embed


def get_clean_name(boss_name) -> str:
    clean_name = str(boss_name.name)
    # Add a space between each uppercase letter
    for i in range(len(clean_name) - 1, 0, -1):
        if clean_name[i].isupper() and clean_name[i - 1].islower():
            clean_name = clean_name[:i] + " " + clean_name[i:]

    return clean_name


def convert_game_ticks_to_time(ticks: int) -> str:
    total_ms = ticks * 600
    minutes, rem_ms = divmod(total_ms, 60_000)
    seconds, ms = divmod(rem_ms, 1_000)
    centiseconds = ms // 10

    return f"{minutes}:{seconds:02}.{centiseconds:02}"
