from transformers import pipeline
from config.parametres import VERSIONS
from model.prompt import Prompt

def traduire(prompt: Prompt):
    translator = None  # Initialisation de la variable translator

    if prompt.version == VERSIONS[0]:  # Cas de la traduction 'fr >> en'
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
    elif prompt.version == VERSIONS[1]:  # Cas de la traduction 'en >> fr'
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

    if translator is not None:
        prompt.traduction = translator(prompt.atraduire)
    else:
        raise ValueError(f"Aucun modèle trouvé pour la version: {prompt.version}")
    
    return prompt
