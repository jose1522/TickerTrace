from decouple import config

DEBUG = config("DEBUG", default=False, cast=bool)
AV_API_KEY = config("AV_API_KEY", default="")
AV_API_URL = config("AV_API_URL", default="https://www.alphavantage.co/query")

# Build database connection url
DB_USER = config("DB_USER", default="")
DB_PASSWORD = config("DB_PASSWORD", default="")
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default="5432")
DB_NAME = config("DB_NAME", default="ticker_trace")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
