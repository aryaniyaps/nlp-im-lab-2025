"""
Part C- mini project

Design and Implementation of a User-Choice Based Multilingual Translation System: 
The problem statement is to design and implement a translation system that accepts text from 
the user and allows the user to choose the target language dynamically. The system should be 
interactive, simple to use, and demonstrate practical NLP-based machine translation. 
"""

from googletrans import Translator
import asyncio

supported_languages = {
    "ta": "tamil",
    "hi": "hindi",
    "fr": "french",
    "de": "german",
    "it": "italian",
    "ja": "japanese",
}

async def run_program():
    while True:
        print("Multilingual Translation System")
        print("Supported Languages:")
        for code, lang in supported_languages.items():
            print(f"{code}: {lang}")
        print("-" * 10)
        
        target = input("Enter target language code: ")
        if supported_languages.get(target) is None:
            print("Invalid target language. Try again.")
        else:
            text = input("Enter source text: ")
            translator = Translator()
            translated = await translator.translate(text, src="en", dest=target)
            print("Translated: ", translated.text)

asyncio.run(run_program())
