
db: Session = next(get_db())
        # iiiii = db.get(Activity).all()
        iiiii = db.query(Activity).all()

results = db.query(Submission).filter(
                Submission.create_time >= cutoff_date
            ).order_by(Submission.create_time.desc()).all()


@app_commands.command(name="get_sample", description="get_sample")
async def get_sample(
    self,
    interaction: discord.Interaction,
):
        
db: Session = next(get_db())

iiiii = db.query(Activity).all()
print(iiiii)

await interaction.response.send_message(f"pong {interaction.user.mention}!", ephemeral=True)