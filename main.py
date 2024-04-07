from googletrans import Translator
import pyttsx3
from flask import Flask,flash, redirect,render_template,request,url_for
import uuid
import os
from flask import render_template,request
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
import openai
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY']='secretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
ALLOWED_EXTENSIONS= {'txt','pdf'}
#API_KEY = open("API_KEY", "r").read()
openai.api_key = os.getenv("API_KEY")
chat_log = [{"role":"system","content":"You should provide well structured notes for the topic given"}]

tts = pyttsx3.init()


def texttospeech(text,record):
    tts.say(text)
    tts.save_to_file(text,record)


def translator(text, language):
    translator = Translator()
    translated = translator.translate(text,dest=language)
    return translated.text


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
    

@app.route("/partner",methods=['POST','GET'])
def aiNote():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        chat_log.append({"role":"user","content": prompt})
        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = chat_log
        )
        notes = response['choices'][0]['message']['content']
        note = notes.strip()
        chat_log.append({"role":"assistant","content": notes})
        print(note)
        return render_template("AiPartner.html", note = note)
    else:
        return render_template("AiPartner.html")


if __name__ == '__main__':
    app.run(debug=True)





