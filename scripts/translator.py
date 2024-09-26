from googletrans import Translator

# Create a Translator object
translator = Translator()  # French for "Hello everyone"

# Translate the text
def translate_text(text, target_language='en'):
    translated = translator.translate(text, dest=target_language)
    return translated.text
