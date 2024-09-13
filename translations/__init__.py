# translations/__init__.py

from .translate_openai import translate_with_openai
from .translate_groq import translate_with_groq
from .translate_ollama import translate_with_ollama
#from .translate_llama3 import translate_with_llama3
from .translate_custom import translate_with_custom

def get_translator(api_name):
    translators = {
        'openai': translate_with_openai,
        'groq': translate_with_groq,
        'ollama': translate_with_ollama,
       # 'llama3': translate_with_llama3,
        'custom': translate_with_custom
    }
    return translators.get(api_name.lower())
