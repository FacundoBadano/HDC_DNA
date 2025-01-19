from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import hashlib
import json
import os

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

# Archivo para almacenar los hipervectores
HV_STORAGE_FILE = "hv_storage.json"

# Cargar el almacenamiento de hipervectores si existe
if os.path.exists(HV_STORAGE_FILE):
    with open(HV_STORAGE_FILE, "r") as f:
        hv_storage = json.load(f)
else:
    hv_storage = {}

# Guardar los hipervectores en el archivo JSON
def save_hv_storage():
    with open(HV_STORAGE_FILE, "w") as f:
        json.dump(hv_storage, f)

# Generar un hash determinista para una secuencia
def generate_hash(sequence):
    return hashlib.md5(sequence.encode()).hexdigest()

# Validar secuencia de ADN
def validate_sequence(sequence):
    valid_chars = {'G', 'T', 'C', 'A'}
    return all(char in valid_chars for char in sequence)

# Codificar una secuencia en un hipervector
def encode_sequence(sequence, hv_dim=1000):
    hash_key = generate_hash(sequence)
    
    # Si ya existe en el almacenamiento, devolver el hipervector guardado
    if hash_key in hv_storage:
        return torch.tensor(hv_storage[hash_key])

    # Calcular el hipervector si no existe
    ngrams = [sequence[i:i+3] for i in range(len(sequence) - 2)]  # n-grams con n=3
    if len(ngrams) == 0:
        raise ValueError("No se pudieron generar n-grams válidos.")
    
    hv = torch.zeros(hv_dim)
    for i, ngram in enumerate(ngrams):
        seed = int(hashlib.md5(ngram.encode()).hexdigest(), 16) % (2**32)
        torch.manual_seed(seed)
        random_hv = torch.randint(0, 2, (hv_dim,)).float() * 2 - 1  # Bipolar random HV
        shifted_hv = torch.roll(random_hv, shifts=i)
        hv += shifted_hv
    
    hv = hv / len(ngrams)  # Normalizar

    # Guardar el hipervector en el almacenamiento
    hv_storage[hash_key] = hv.tolist()
    save_hv_storage()

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
