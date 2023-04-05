import discord
from discord import app_commands
from dbconnector import connectdb


id_do_servidor = 510242958113505290  # Coloque aqui o ID do seu servidor


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        # Nós usamos isso para o bot não sincronizar os comandos mais de uma vez
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Checar se os comandos slash foram sincronizados
            # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            await tree.sync(guild=discord.Object(id=id_do_servidor))
            self.synced = True
        print(f"Entramos como {self.user}.")


aclient = client()
tree = app_commands.CommandTree(aclient)


@tree.command(guild=discord.Object(id=id_do_servidor), name='updatedatabase', description='Atualiza os dados selecionados no banco de dados')
async def updatedatabase(interaction: discord.Interaction, host: str, database: str, user: str, password: str):

    await interaction.response.send_message(f"mensagens: {host} {database} {user} {password}")

    connectdb(host, database, user, password)

# Comando específico para seu servidor


@tree.command(guild=discord.Object(id=id_do_servidor), name='teste', description='Testando')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"Estou funcionando!", ephemeral=True)

aclient.run(
    'MTA5MDEyMjY4MDA5Njc5NjczNw.GBugHa.3cn_7L-8QLaJJKlMc4QgLQPjDbul0vpmhiC0Tw')
