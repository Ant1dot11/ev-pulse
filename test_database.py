from database import *

init_db()

add_published(
    "https://test.com",
    "Tesla Test",
    "Electrek",
    95
)

print(is_published("https://test.com"))

print(get_statistics())