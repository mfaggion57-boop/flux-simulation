import pandas as pd
from datetime import datetime
import random

CSV_FILE = "compteurs.csv"

# Ajouter une nouvelle ligne
new_row = {
    "timestamp": datetime.now(),
    "humains": random.randint(0, 100),
    "velos": random.randint(0, 50)
}

# Lire le CSV existant ou créer un DataFrame vide
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["timestamp", "humains", "velos"])

# Ajouter la nouvelle ligne
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Sauvegarder le CSV
df.to_csv(CSV_FILE, index=False)

print(f"{datetime.now()}: ligne ajoutée")