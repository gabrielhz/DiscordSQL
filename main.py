import discord
import dbconnector
import api
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
    dbconnector.cfg_save(
        'db.cfg', f"{host}", f"{database}", f"{user}", "")
    await interaction.response.send_message(dbconnector.list_tables(dbconnector.cfg_read('host'), dbconnector.cfg_read('database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password')), ephemeral=True)


@tree.command(guild=discord.Object(id=id_do_servidor), name='tables', description='Tabelas disponíveis')
async def tables(interaction: discord.Interaction):
    await interaction.response.send_message(dbconnector.list_tables(dbconnector.cfg_read('host'), dbconnector.cfg_read('database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password')), ephemeral=True)
    dbconnector.disconnectdb()


@tree.command(guild=discord.Object(id=id_do_servidor), name='columns', description='Colunas disponíveis')
async def tables(interaction: discord.Interaction, tableid: str,):
    await interaction.response.send_message(dbconnector.list_columns(dbconnector.cfg_read('host'), dbconnector.cfg_read('database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password'), tableid), ephemeral=True)
    dbconnector.disconnectdb()


@tree.command(guild=discord.Object(id=id_do_servidor), name='updatedatabase', description='Modifica os dados da tabela selecionada')
async def updatedatabase(interaction: discord.Interaction, tableid: str, steamid: str, row: str, newvalue: str):
    dbconnector.connectdb(dbconnector.cfg_read('host'), dbconnector.cfg_read(
        'database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password'))
    dbconnector.updatedb(tableid, steamid, row, newvalue)
    dbconnector.disconnectdb()
    await interaction.response.send_message(f"On database {dbconnector.cfg_read('database')} \ntable: {tableid} \nupdated {row} row on steamid {steamid} to {newvalue}", ephemeral=True)


@tree.command(guild=discord.Object(id=id_do_servidor), name='rows', description='Campos no banco de dados')
async def rows(interaction: discord.Interaction, tableid: str):
    rows = dbconnector.list_rows(tableid, dbconnector.cfg_read('host'), dbconnector.cfg_read(
        'database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password'))

    embed = discord.Embed(title=f"{tableid}",
                          description="", colour=discord.Colour.purple())
    embed.set_author(name="discord.sql")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
    embed.set_footer(text=api.get_latest_version())
    i = 0
    while i < len(rows):
        key = list(rows.keys())[i]
        values = rows[key]
        values_str = ', '.join(str(v) for v in values)
        embed.add_field(name=f"{key}", value=f"{values_str}")
        i = i + 1

    await interaction.response.send_message(embed=embed)


@tree.command(guild=discord.Object(id=id_do_servidor), name='row', description='Campos no banco de dados')
async def row(interaction: discord.Interaction, tableid: str, steamid: str):
    row = dbconnector.list_unique_rows(tableid, steamid, dbconnector.cfg_read('host'), dbconnector.cfg_read(
        'database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password'))

    embed = discord.Embed(title=f"{tableid}",
                          description="", colour=discord.Colour.purple())
    embed.set_author(name="discord.sql")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
    embed.set_footer(text=api.get_latest_version())
    i = 0
    while i < len(row):
        key = list(row.keys())[i]
        value = row[key]
        value_str = ', '.join(str(v) for v in value)
        embed.add_field(name=f"{key}", value=f"{value_str}")
        i = i + 1

    await interaction.response.send_message(embed=embed)


@tree.command(guild=discord.Object(id=id_do_servidor), name='sqlcommand', description='Campos no banco de dados')
async def sqlcommand(interaction: discord.Interaction, command: str):
    row = dbconnector.run_command(command, dbconnector.cfg_read('host'), dbconnector.cfg_read(
        'database'), dbconnector.cfg_read('user'), dbconnector.cfg_read('password'))

    embed = discord.Embed(title=f"{row[0]}",
                          description="", colour=discord.Colour.purple())
    embed.set_author(name="discord.sql")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
    embed.set_footer(text=api.get_latest_version())

    embed.add_field(name=f"Command return:", value=f"{row[1]}")

    await interaction.response.send_message(embed=embed)


aclient.run(
    'MTA5MDEyMjY4MDA5Njc5NjczNw.Gw_TYC.ALOQoW9J_Mg66oyPqwR_NXFLBUunlPSwciZmS4')
