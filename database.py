from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

# Encodage sécurisé des paramètres
username = quote_plus("postgres")
password = quote_plus("rym")
host = quote_plus("localhost")
dbname = quote_plus("quizapp")

URL_DATABASE = f"postgresql://{username}:{password}@{host}:5433/{dbname}"

engine = create_engine(
    URL_DATABASE,
    pool_pre_ping=True,  # Vérifie la connexion avant utilisation
    echo=True  # Active les logs SQL (utile pour le débogage)
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()