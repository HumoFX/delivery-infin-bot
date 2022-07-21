from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.int("ADMIN_ID")  # Тут у нас будет список из админов
# IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
LOGS_CHANNEL = -1001644884708
ADMIN_GROUP = -1001530214778

POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_HOST = env.str("POSTGRES_HOST")
HTTP_PROXY = env.str("HTTP_PROXY")
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

