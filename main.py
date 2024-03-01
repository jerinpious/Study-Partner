from googletrans import Translator
import pyttsx3


tts = pyttsx3.init()


def texttospeech(text):
    tts.say(text)
    tts.runAndWait()

def translator(text, language):
    translator = Translator()
    translated = translator.translate(text,dest=language)
    return translated.text


languages=['en','fr','nl','ar','de']

print("\nChoose the language to translate into..")
print("1. English\n2. French\n3. Dutch\n4. Arabic\n5. German\n")
choice = int(input("Choose an option: "))
language = languages[choice-1]
text = input("What would you like to translate>> ")

output = translator(text, language)

texttospeech(output)

print(output)


