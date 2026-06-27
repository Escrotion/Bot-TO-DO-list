import aiosqlite

DB_PATH = "database/tasks.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'Por hacer',
                priority TEXT DEFAULT 'Media',
                due_date TEXT,
                tag TEXT
            )
        """)
        await db.commit()