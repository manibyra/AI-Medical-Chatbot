# translator.py
from googletrans import Translator

translator = Translator()

def translate_text(text, src='auto', dest='en'):
    try:
        result = translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception as e:
        return f"[Translation Error] {e}"
