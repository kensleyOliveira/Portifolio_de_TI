import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")  # caminho para o .env

MYSQL_DSN = os.getenv(
    "MYSQL_DSN",
    "mysql+pymysql://user:password@localhost:3306/b3dw"  # fallback
)

# Diretório base para os dados
DATA_DIR = os.getenv("DATA_DIR", "./data")

# Timezone padrão
TZ = os.getenv("TZ", "America/Sao_Paulo")

# Lista de tickers default (~60 da B3)
TICKERS = os.getenv("TICKERS",
    "ABEV3.SA,ALPA4.SA,ALUP11.SA,AMER3.SA,ASAI3.SA,AZZA3.SA,"
    "B3SA3.SA,BBAS3.SA,BBDC4.SA,BBSE3.SA,BOVA11.SA,BPAC11.SA,"
    "CASH3.SA,CBAV3.SA,MOVT3.SA,CSAN3.SA,CSMG3.SA,CSNA3.SA,"
    "CVCB3.SA,CYRE3.SA,ECOR3.SA,ELET3.SA,EQTL3.SA,GGBR4.SA,"
    "HAPV3.SA,IGTI11.SA,INBR32.SA,INTB3.SA,ITSA4.SA,ITUB4.SA,"
    "JBSS3.SA,LREN3.SA,MGLU3.SA,MRFG3.SA,MRVE3.SA,MTRE3.SA,"
    "MULT3.SA,NATU3.SA,PETR4.SA,POMO4.SA,PRIO3.SA,PSSA3.SA,"
    "RADL3.SA,RAIL3.SA,RDOR3.SA,RENT3.SA,SANB11.SA,SBSP3.SA,"
    "SEER3.SA,SLCE3.SA,SUZB3.SA,TOTS3.SA,VALE3.SA,VBBR3.SA,"
    "VIVT3.SA,WEGE3.SA"
).split(",")
