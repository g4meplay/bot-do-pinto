from database.engine import Session
from database.models import User
import discord
from discord.ui import View

class PaginatedUserRank(View):
    def __init__(
        self,
        interaction: discord.Interaction | None = None,
        *,
        client: discord.Client | None = None,
        channel: discord.TextChannel | None = None,
        page: int = 1,
        per_page: int = 5,
        timeout: float = 180
    ):
        super().__init__(timeout=timeout)
        self.page = page
        self.per_page = per_page
        self.interaction = interaction
        self.client = client or (interaction.client if interaction else None)
        self.channel = channel
        self.message = None  # Referência à mensagem enviada

        if self.client is None:
            raise ValueError("O cliente deve ser fornecido se a interação for None.")

    async def fetch_user_data(self):
        offset = (self.page - 1) * self.per_page
        with Session() as session:
            media = (User.min + User.avg + User.max) / 3
            users = (
                session.query(User, media.label("media"))
                .order_by(media.desc())
                .offset(offset)
                .limit(self.per_page)
                .all()
			)
        return users

    async def get_page_count(self):
        with Session() as session:
            total_users = session.query(User).count()
        return (total_users // self.per_page) + (1 if total_users % self.per_page else 0)

    async def display_data(self):
        users = await self.fetch_user_data()
        page_count = await self.get_page_count()

        embed = discord.Embed(
            title="Ranking dos Pintos",
            description=f"**Página {self.page}/{page_count}**",
            color=discord.Color.gold()
        )

        for user, _ in users:
            guild = self.interaction.guild if self.interaction else self.channel.guild
            user_profile = guild.get_member(user.id) if guild else None

            if user_profile:
                user_avatar_url = user_profile.avatar.url if user_profile.avatar else None
                embed.add_field(
                    name=f"Usuário: @{user_profile.name}",
                    value=f"Broxa: {user.min} cm\nMeia bomba: {user.avg} cm\nDuro: {user.max} cm",
                    inline=False
                )
                if user_avatar_url and not embed.thumbnail:
                    embed.set_thumbnail(url=user_avatar_url)

        try:
            # Se houver uma interação (slash command)
            if self.interaction:
                if not self.interaction.response.is_done():
                    await self.interaction.response.send_message(embed=embed, view=self)
                    self.message = await self.interaction.original_response()
                else:
                    await self.message.edit(embed=embed, view=self)
            # Se não houver interação (prefix command)
            elif self.channel:
                if self.message:
                    await self.message.edit(embed=embed, view=self)
                else:
                    self.message = await self.channel.send(embed=embed, view=self)
        except Exception as e:
            print(f"Erro ao enviar/editar mensagem: {e}")

    async def start(self):
        """Inicia a exibição do ranking."""
        await self.display_data()

    @discord.ui.button(label="Próxima Página", style=discord.ButtonStyle.green)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        page_count = await self.get_page_count()
        if self.page < page_count:
            self.page += 1
            await self.display_data()
        else:
            await interaction.response.send_message("Você já está na última página.", ephemeral=True)
        await interaction.response.defer()

    @discord.ui.button(label="Página Anterior", style=discord.ButtonStyle.red)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
            await self.display_data()
        else:
            await interaction.response.send_message("Você já está na primeira página.", ephemeral=True)
        await interaction.response.defer()