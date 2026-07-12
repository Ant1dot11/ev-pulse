from database import (
    init_db,
    is_published,
    add_published,
)

# Создаем базу автоматически при запуске
init_db()

all = [
    "is_published",
    "add_published",
]