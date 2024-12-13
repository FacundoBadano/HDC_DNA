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
class DNASequence(BaseModel):
    sequence: str

# Validar secuencia de ADN
def validate_sequence(sequence):
    valid_chars = {'G', 'T', 'K', 'A'}
    return all(char in valid_chars for char in sequence)

@app.post("/generate-hv")
async def create_hv(data: DNASequence):
    if not validate_sequence(data.sequence):
        raise HTTPException(status_code=400, detail="La secuencia contiene caracteres inválidos.")

    if len(data.sequence) < 3:
        raise HTTPException(status_code=400, detail="La secuencia debe tener al menos 3 caracteres.")

    hv_dim = 1000  # Dimensión del hipervector
    ngrams = [data.sequence[i:i+3] for i in range(len(data.sequence) - 2)]  # n-grams con n=3

    if len(ngrams) == 0:
        raise HTTPException(status_code=400, detail="No se pudieron generar n-grams válidos.")

    hv = torch.zeros(hv_dim)
    for ngram in ngrams:
        random_hv = torch.randint(0, 2, (hv_dim,)).float() * 2 - 1  # Bipolar random HV
        hv += random_hv

    hv = hv / len(ngrams)  # Normalizar

    # Limpia valores no válidos
    hv_list = hv.tolist()
    hv_list = [0 if (val != val or val == float("inf") or val == float("-inf")) else val for val in hv_list]

    return {"hypervector": hv_list}
