from fastapi import FastAPI
from pydantic import BaseModel
import pymorphy2
from typing import List

app = FastAPI()
morph = pymorphy2.MorphAnalyzer()

class LemmaResponse(BaseModel):
    lemma: str
    part_of_speech: str

class TextInput(BaseModel):
    text: str

@app.post("/lemmatize", response_model=List[LemmaResponse])
async def lemmatize(input: TextInput):
    text = input.text
    words = text.split()
    results = []

    for word in words:
        parsed_word = morph.parse(word)
        # Извлекаем леммы и части речи
        lemmas = [{'lemma': p.normal_form, 'part_of_speech': str(p.tag)} for p in parsed_word]
        results.extend(lemmas)

    return results