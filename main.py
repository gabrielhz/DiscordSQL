import discord
import dbconnector
from discord import app_commands

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


@tree.command(guild=discord.Object(id=id_do_servidor), name='setdatabase', description='Atualiza os dados do banco de dados')
async def setdatabase(interaction: discord.Interaction, host: str, database: str, user: str, password: str):
    # await interaction.response.send_message(f"mensagens: {host} {database} {user} {password}")
    dbconnector.cfg_save(
        'db.cfg', f"{host}", f"{database}", f"{user}", "")
    await interaction.response.send_message(dbconnector.list_tables(dbconnector.cfg_read('host'), dbconnector.cfg_read('database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password')), ephemeral=True)


@tree.command(guild=discord.Object(id=id_do_servidor), name='tables', description='Tabelas disponíveis')
async def tables(interaction: discord.Interaction):
    await interaction.response.send_message(dbconnector.list_tables(dbconnector.cfg_read('host'), dbconnector.cfg_read('database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password')), ephemeral=True)
    dbconnector.disconnectdb()


@tree.command(guild=discord.Object(id=id_do_servidor), name='rows', description='Colunas disponíveis')
async def tables(interaction: discord.Interaction, tableid: str,):
    await interaction.response.send_message(dbconnector.list_rows(dbconnector.cfg_read('host'), dbconnector.cfg_read('database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password'), tableid), ephemeral=True)
    dbconnector.disconnectdb()


@tree.command(guild=discord.Object(id=id_do_servidor), name='updatedatabase', description='Modifica os dados da tabela selecionada')
async def updatedatabase(interaction: discord.Interaction, tableid: str, steamid: str, row: str, newvalue: str):
    dbconnector.connectdb(dbconnector.cfg_read('host'), dbconnector.cfg_read(
        'database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password'))
    dbconnector.updatedb(tableid, steamid, row, newvalue)
    dbconnector.disconnectdb()
    await interaction.response.send_message(f"On database {dbconnector.cfg_read('database')} \ntable: {tableid} \nupdated {row} row on steamid {steamid} to {newvalue}", ephemeral=True)


aclient.run(
    'MTA5MDEyMjY4MDA5Njc5NjczNw.GBugHa.3cn_7L-8QLaJJKlMc4QgLQPjDbul0vpmhiC0Tw')
