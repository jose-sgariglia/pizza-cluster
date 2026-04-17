import pandas as pd
import urllib.parse # Questa libreria serve per pulire gli URL

df = pd.read_parquet('data/raw/documenti_sample_5000.parquet')
base_url = "https://assets.getkino.com/"

# Funzione per codificare correttamente il percorso (trasforma spazi in %20)
def pulisci_url(path):
    percorso_pulito = str(path).strip()
    # Usiamo quote per gestire spazi e parentesi, ma lasciamo le / intatte
    return base_url + urllib.parse.quote(percorso_pulito, safe='/')

# Creiamo i link sicuri
links = df['path'].apply(pulisci_url)

# Salviamo la lista
links.to_csv('lista_link_sicuri.txt', index=False, header=False)

print("Esempio di link codificato:")
print(links.iloc[0])