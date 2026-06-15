import requests
import logging
from typing import List

def get_llm_cluster_name(keywords: List[str], model: str = "llama3") -> str:
    """
    Given a list of keywords, use a local Ollama LLM to generate a short, 
    1-2 word descriptive name for the cluster.
    Assumes Ollama is running locally at http://localhost:11434.
    """
    if not keywords:
        return "Noise / Unknown"
        
    url = "http://localhost:11434/api/chat"
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a specialized keyword summarizer. You must output EXACTLY ONE SHORT NAME (max 3 words) and absolutely nothing else. Stop immediately after the name."
            },
            {
                "role": "user",
                "content": "Keywords: apple, banana, fruit, market"
            },
            {
                "role": "assistant",
                "content": "Fruit Market"
            },
            {
                "role": "user",
                "content": "Keywords: car, engine, tires, driving"
            },
            {
                "role": "assistant",
                "content": "Automobiles"
            },
            {
                "role": "user",
                "content": f"Keywords: {', '.join(keywords)}"
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.0,  # Zero assoluto per azzerare la creatività
        }
    }
    
    try:
        # Timeout aumentato a 180s per permettere a Ollama di caricare il modello in memoria la prima volta
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()
        result = response.json()
        name = result.get("message", {}).get("content", "").strip()
        
        # Clean up possible markdown artifacts, quotes or trailing periods
        name = name.strip('"').strip("'").strip('*').strip('.')
        return name
    except Exception as e:
        logging.error(f"Error calling Ollama API for model {model}: {e}")
        # Fallback to the top 2 keywords if the API fails
        return " / ".join(keywords[:2]) if len(keywords) >= 2 else keywords[0]

if __name__ == "__main__":
    # Test rapido di connessione a Ollama locale
    test_keywords = ["flight", "private jet", "travel", "epstein", "airport", "schedule"]
    print("Test connessione a Ollama in locale in corso...")
    print(f"Keyword di test: {test_keywords}")
    
    try:
        print("Invocazione modello... (potrebbe richiedere qualche secondo se deve essere caricato in RAM)")
        # Utilizza il modello di default indicato nel file
        risultato = get_llm_cluster_name(test_keywords)
        print("\n--- RISULTATO ---")
        print(f"Nome generato: '{risultato}'")
        print("-----------------")
        if "/" in risultato and "flight" in risultato:
            print("\nAttenzione: il risultato sembra essere il fallback. Controlla i log per vedere se Ollama ha restituito un errore (es. modello non trovato o server non attivo).")
    except Exception as e:
        print(f"\nERRORE CRITICO: {e}")
        print("Assicurati che Ollama sia in esecuzione (eseguire 'ollama serve') e che il modello sia stato scaricato ('ollama run qwen3.5' o 'llama3').")
