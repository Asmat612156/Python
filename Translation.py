import gradio as gr
import googletrans
import speech_recognition
from gtts import gTTS
import os
import base64

# Define a function to perform speech translation & Text translation
def translate_speech(task, audio_source, input_text, source_language, target_language):
    if audio_source == "microphone":
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            print("Speak Now")
            voice = recognizer.listen(source)
            input_text = recognizer.recognize_google(voice, language=source_language)

    translator = googletrans.Translator()
    translation = translator.translate(input_text, dest=target_language)

    if task == "T2ST (Text to Speech translation)":
        tts = gTTS(text=translation.text, lang=target_language, slow=False)
        audio_filename = "translated_audio.mp3"
        tts.save(audio_filename)

        # Encode the audio file to base64 for embedding in HTML
        with open(audio_filename, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode()

        audio_player_html = f'<audio controls><source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
        return audio_player_html
    return translation.text
  
# Create a Gradio interface


iface = gr.Interface(   
    fn=translate_speech,
    inputs=[
        gr.inputs.Dropdown(
            ["S2ST (Speech to Text translation)", "S2TT (Speech to Text translation)", 
             "T2ST (Text to Speech translation)", "T2TT (Text to Text translation)", "ASR (Automatic Speech Recognition)"],
            label="Task"
        ),
        gr.inputs.Radio(["microphone", "text"], label="Audio Source"),
        gr.inputs.Textbox(label="Input Text"),
        gr.inputs.Dropdown(
            ["en", "es", "fr", "de", "it", "ja", "ko", "zh-CN", "ru", "ar", "hi"],
            label="Source Language"
        ),
        gr.inputs.Dropdown(
            ["en", "es", "fr", "de", "it", "ja", "ko", "zh-CN", "ru", "ar", "hi","ur"],
            label="Target Language"
        )
    ],
    outputs=gr.outputs.HTML(label="Translated Audio"),

    title="Translation Web Application",
    description="NED Academy Batch IV Asmat Mehmood",
)

# Launch the Gradio interface
iface.launch()
