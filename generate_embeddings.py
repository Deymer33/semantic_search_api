import os
import pickle
import pandas as pd
import mysql.connector
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener datos de conexión desde variables de entorno
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Conectarse a la base de datos
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

# Leer herramientas desde la base de datos
cursor.execute("SELECT id, name, description, link FROM tools")
rows = cursor.fetchall()
cursor.close()
conn.close()

# Convertir a DataFrame
df = pd.DataFrame(rows)

# Eliminar duplicados por descripción
df = df.drop_duplicates(subset="description")

# Generar embeddings
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
descriptions = df['description'].tolist()
embeddings = model.encode(descriptions, show_progress_bar=True)

# Guardar embeddings y DataFrame
with open('embeddings.pkl', 'wb') as f:
    pickle.dump((df, embeddings), f)

print(" Embeddings generados desde la base de datos y guardados.")
