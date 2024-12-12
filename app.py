# backend/app.py
def generate_ngrams(sequence, n):
  ngrams = []
  for i in range(len(sequence) - n + 1):
    ngrams.append(sequence[i:i+n])
  return ngrams