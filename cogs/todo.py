import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database.db import init_db, DB_PATH

class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await init_db()
        print("✅ Base de datos lista")

    @app_commands.command(name="add", description="Añade una nueva tarea")
    @app_commands.describe(nombre="Nombre de la tarea")
    async def add(self, interaction: discord.Interaction, nombre: str):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("INSERT INTO tasks (name) VALUES (?)", (nombre,))
            await db.commit()
        await interaction.response.send_message(f"✅ Tarea **{nombre}** añadida!")

    @app_commands.command(name="list", description="Muestra todas las tareas")
    async def list_tasks(self, interaction: discord.Interaction):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute("SELECT id, name, status, priority FROM tasks") as cursor:
                tasks = await cursor.fetchall()

        if not tasks:
            await interaction.response.send_message("📭 No tienes tareas pendientes.")
            return

        embed = discord.Embed(title="📋 Tus tareas", color=0x5865F2)
        for task in tasks:
            id, name, status, priority = task
            emoji = {"Por hacer": "⬜", "Hecho": "✅", "Pospuesto": "⏸️"}.get(status, "⬜")
            embed.add_field(
                name=f"{emoji} #{id} — {name}",
                value=f"Estado: `{status}` | Prioridad: `{priority}`",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="done", description="Marca una tarea como hecha")
    @app_commands.describe(id="ID de la tarea")
    async def done(self, interaction: discord.Interaction, id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("UPDATE tasks SET status = 'Hecho' WHERE id = ?", (id,))
            await db.commit()
        await interaction.response.send_message(f"✅ Tarea #{id} marcada como **Hecha**!")

    @app_commands.command(name="remove", description="Elimina una tarea")
    @app_commands.describe(id="ID de la tarea")
    async def remove(self, interaction: discord.Interaction, id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("DELETE FROM tasks WHERE id = ?", (id,))
            await db.commit()
        await interaction.response.send_message(f"🗑️ Tarea #{id} eliminada.")

    @app_commands.command(name="status", description="Cambia el estado de una tarea")
    @app_commands.describe(id="ID de la tarea", estado="Nuevo estado")
    @app_commands.choices(estado=[
        app_commands.Choice(name="Por hacer", value="Por hacer"),
        app_commands.Choice(name="Hecho", value="Hecho"),
        app_commands.Choice(name="Pospuesto", value="Pospuesto"),
    ])
    async def status(self, interaction: discord.Interaction, id: int, estado: str):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("UPDATE tasks SET status = ? WHERE id = ?", (estado, id))
            await db.commit()
        await interaction.response.send_message(f"🔄 Tarea #{id} actualizada a **{estado}**!")

async def setup(bot):
    await bot.add_cog(Todo(bot))