import settings
import views

from database.engine import Session
from database.models import User
from database.migrations import migrate

import discord
from discord.ext.commands import Bot, Context

intents = discord.Intents.all()  # Permissions
bot = Bot(command_prefix=">", intents=intents)  # Client

@bot.command(name="pinto")
async def pinto(context: Context, broxa: float, meia_bomba: float, duro: float):
	"""
	Registra e edita o modelo `User`.
	Retornos vazios são usados para No-op. Caso contrário, no `if`,
	o fluxo saltaria para o corpo de baixo.

	Ass: @pavelixo
	"""

	# Desempacotando `id do autor` e `session`
	id, session = (
		context.author.id, Session()
	)

	# Inicializador do Embed
	embed = discord.Embed(
		title="Informações sobre sua caceta", 
		color=discord.Color.red()
	)
	
	# Consulta do usuário
	user = session.query(User).filter_by(id=id).first()

	if user is not None:
		# Modelo do usuário
		user.min = broxa; user.avg = meia_bomba; user.max = duro
		
		# Dados no embed
		embed.add_field(name="Broxa:", value=f"{user.min} cm")
		embed.add_field(name="Meia Bomba:", value=f"{user.avg} cm")
		embed.add_field(name="Duro:", value=f"{user.max} cm")

		# Commit
		session.commit(); session.close()

		await context.reply(
			"Você editou sua peça.",
			embed=embed
		)
		return
	
	# Modelo do usuário
	user = User(id=id, min=broxa, avg=meia_bomba, max=duro)

	# Dados no embed
	embed.add_field(name="Broxa", value=user.min)
	embed.add_field(name="Meia Bomba", value=user.avg)
	embed.add_field(name="Duro", value=user.max)

	# Commit
	session.add(user); session.commit(); session.close()

	await context.reply(
		"Peça registrada.",
		embed=embed
	)
	return

@bot.command()
async def pintos(ctx):
    view = views.PaginatedUserRank(client=ctx.bot, channel=ctx.channel, per_page=2)
    await view.start()  # Inicia manualmente o processo

@bot.event
async def on_ready():
	"""
	Roda as migrações toda vez que o bot é iniciado.
	"""

	migrate()

if __name__ == "__main__":
	bot.run(token=settings.TOKEN)
