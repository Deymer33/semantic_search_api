import os
import pickle
import pymysql
import pandas as pd
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def generar_embeddings():
    print("🔄 Conectando a la base de datos...")
    conn = pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )

    query = "SELECT description, link FROM tools"
    df = pd.read_sql(query, conn)
    conn.close()

    print(f"📊 {len(df)} herramientas encontradas.")

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(df['description'].tolist(), show_progress_bar=True)

    with open("/app/data/embeddings.pkl", "wb") as f:
        pickle.dump((df, embeddings), f)

    print("✅ Embeddings regenerados y guardados.")

if __name__ == "__main__":
    generar_embeddings()
