from googletrans import Translator
import pyttsx3
from flask import Flask
import uuid
import os
from flask import render_template,request


tts = pyttsx3.init()


def texttospeech(text,record):
    tts.say(text)
    tts.save_to_file(text,record)


def translator(text, language):
    translator = Translator()
    translated = translator.translate(text,dest=language)
    return translated.text

app = Flask(__name__)
@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/translate", methods=['GET','POST'])
def translate():
    
    translated = ""
    if request.method=="POST":
        text = request.form.get("text_to_transalte")
        translated=translator(text,'fr')
        print(translated)
    return render_template('translate.html', translated=translated)

@app.route("/speech",methods=['POST','GET'])
def speech():
    
    if request.method == "POST":
        text = request.form.get("text_to_speech")
        filename = str(uuid.uuid4()) + ".mp3"
        record_path = os.path.join("static", "records", filename)
        texttospeech(text, record_path)
        return render_template('speech.html', audio_file=record_path)
    else:
        return render_template('speech.html')

if __name__ == '__main__':
    app.run(debug=True)

# languages=['en','fr','nl','ar','de']



