from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch

# Crear instancia de FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Cambia "*" a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para recibir datos
class DNASequences(BaseModel):
    sequence1: str
    sequence2: str

# Validar secuencia de ADN
def validate_sequence(sequence):
    valid_chars = {'G', 'T', 'C', 'A'}
    return all(char in valid_chars for char in sequence)

# Codificar una secuencia en un hipervector
def encode_sequence(sequence, hv_dim=1000):
    ngrams = [sequence[i:i+3] for i in range(len(sequence) - 2)]  # n-grams con n=3
    if len(ngrams) == 0:
        raise ValueError("No se pudieron generar n-grams válidos.")
    
    hv = torch.zeros(hv_dim)
    for ngram in ngrams:
        random_hv = torch.randint(0, 2, (hv_dim,)).float() * 2 - 1  # Bipolar random HV
        hv += random_hv
    
    hv = hv / len(ngrams)  # Normalizar
    return hv

# Endpoint para calcular la distancia entre dos secuencias
@app.post("/generate-hv")
async def calculate_distance(data: DNASequences):
    # Validar las secuencias
    if not validate_sequence(data.sequence1) or not validate_sequence(data.sequence2):
        raise HTTPException(status_code=400, detail="Una o ambas secuencias contienen caracteres inválidos.")
    
    # Codificar ambas secuencias
    try:
        hv1 = encode_sequence(data.sequence1)
        hv2 = encode_sequence(data.sequence2)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Calcular la distancia del coseno
    distance = 1 - torch.cosine_similarity(hv1, hv2, dim=0).item()
    return {"distance": distance}
