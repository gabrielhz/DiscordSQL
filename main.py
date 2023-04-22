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

    storing = dbconnector.storedb(
        f"{host}", f"{database}", f"{user}", f"")

    if storing[0] == True:

        tables = dbconnector.list_tables(
            dbconnector.host, dbconnector.database, dbconnector.user, dbconnector.password)

        embed = discord.Embed(title=f"Sucessful connection try at {host} {database} using {user} user.",
                              description=f"Connection info stored", colour=discord.Colour.purple())
        embed.set_author(name="discord.sql")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
        embed.set_footer(text=api.get_latest_version())
        i = 0
        while i < len(tables):
            value = tables[i]
            embed.add_field(name=f"{value}", value=f"")
            i = i + 1

        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title=f"Failed connection try at {host} {database} using {user} user.", description=f"{storing[1]}", colour=discord.Colour.purple())
        embed.set_author(name="discord.sql")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
        embed.set_footer(text=api.get_latest_version())
        await interaction.response.send_message(embed=embed)


@tree.command(guild=discord.Object(id=id_do_servidor), name='tables', description='Tabelas disponíveis')
async def tables(interaction: discord.Interaction):

    tables = dbconnector.list_tables(
        dbconnector.host, dbconnector.database, dbconnector.user, dbconnector.password)

    embed = discord.Embed(title=f"{dbconnector.database} tables",
                          description="", colour=discord.Colour.purple())
    embed.set_author(name="discord.sql")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
    embed.set_footer(text=api.get_latest_version())
    i = 0
    while i < len(tables):
        value = tables[i]
        embed.add_field(name=f"{value}", value=f"")
        i = i + 1

    await interaction.response.send_message(embed=embed)


@tree.command(guild=discord.Object(id=id_do_servidor), name='columns', description='Colunas disponíveis')
async def tables(interaction: discord.Interaction, tableid: str,):

    columns = dbconnector.list_columns(
        tableid, dbconnector.host, dbconnector.database, dbconnector.user, dbconnector.password)

    embed = discord.Embed(title=f"{tableid} columns",
                          description="", colour=discord.Colour.purple())
    embed.set_author(name="discord.sql")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
    embed.set_footer(text=api.get_latest_version())
    i = 0
    while i < len(columns):
        value = columns[i]
        embed.add_field(name=f"{value}", value=f"")
        i = i + 1

    await interaction.response.send_message(embed=embed)

    # await interaction.response.send_message(dbconnector.list_columns(dbconnector.host, dbconnector.database, dbconnector.user, dbconnector.password, tableid), ephemeral=True)


@tree.command(guild=discord.Object(id=id_do_servidor), name='updatedatabase', description='Modifica os dados da tabela selecionada')
async def updatedatabase(interaction: discord.Interaction, tableid: str, steamid: str, row: str, newvalue: str):

    updated = dbconnector.updatedb(tableid, steamid, row, newvalue, dbconnector.host,
                                   dbconnector.database, dbconnector.user, dbconnector.password)

    embed = discord.Embed(title=f"{dbconnector.database} in {tableid}",
                          description="", colour=discord.Colour.purple())
    embed.set_author(name="discord.sql")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
    embed.set_footer(text=api.get_latest_version())

    value = updated[row]
    value_str = ', '.join(str(v) for v in value)

    embed.add_field(name=f"{row}", value=f"{value_str} to {newvalue}")
    embed.add_field(name=f"User", value=f"{steamid}")

    await interaction.response.send_message(embed=embed)
    # await interaction.response.send_message(f"On database {dbconnector.database} \ntable: {tableid} \nupdated {row} row on steamid {steamid} to {newvalue}", ephemeral=True)


@tree.command(guild=discord.Object(id=id_do_servidor), name='rows', description='Campos no banco de dados')
async def rows(interaction: discord.Interaction, tableid: str):
    rows = dbconnector.list_rows(
        tableid, dbconnector.host, dbconnector.database, dbconnector.user, dbconnector.password)

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
    row = dbconnector.list_unique_rows(
        tableid, steamid, dbconnector.host, dbconnector.database, dbconnector.user, dbconnector.password)

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

    row = dbconnector.run_command(
        command, dbconnector.host, dbconnector.database, dbconnector.user, dbconnector.password)

    embed = discord.Embed(title=f"{row[0]}",
                          description="", colour=discord.Colour.purple())
    embed.set_author(name="discord.sql")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
    embed.set_footer(text=api.get_latest_version())

    embed.add_field(name=f"Command return:", value=f"{row[1]}")

    await interaction.response.send_message(embed=embed)


@tree.command(guild=discord.Object(id=id_do_servidor), name='database', description='Campos no banco de dados')
async def database(interaction: discord.Interaction):

    embed = discord.Embed(title=f"using {dbconnector.database} database ",
                          description="", colour=discord.Colour.purple())
    embed.set_author(name="discord.sql")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/981184461322465290/1098046630411911178/discordsqlbanner.png")
    embed.set_footer(text=api.get_latest_version())

    embed.add_field(
        name=f"", value=f"to use another database, please use /setdatabase")

    await interaction.response.send_message(embed=embed)


aclient.run(
    'MTA5MDEyMjY4MDA5Njc5NjczNw.Gw_TYC.ALOQoW9J_Mg66oyPqwR_NXFLBUunlPSwciZmS4')
