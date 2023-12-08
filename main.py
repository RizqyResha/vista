import os
import webbrowser
import openai
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import sounddevice as sd
import os
import pygame
import requests
from bs4 import BeautifulSoup
import json
import re

# Set your OpenAI API key here

openai.api_key = "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"

# Global variable to store audio data
audio = []


def new_record_audio():
    # to record audio as wav file
    print("Recording... Press 's' to stop.")
    fs = 44100
    seconds = 6
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    audio_name = "mysound"
    write(f'./{audio_name}.mp3', fs, myrecording)  # Save as WAV file
    print("Recording stopped.")
    return f'./{audio_name}.mp3'


def transcribe_audio(audio_path):
    print("entered transcribe", "./" + audio_path)
    audio_file = open(audio_path, "rb")
    print(audio_file)
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)
    return transcript['text']


def playmusic(search):
    response = requests.get("https://www.youtube.com/results?search_query="+search).text

    soup = BeautifulSoup(response, 'lxml')
    script = soup.find_all("script")[35]

    json_text = re.search("var ytInitialData = (.+)[,;]{1}", str(script)).group(1)
    json_data = json.loads(json_text)

    content = (
        json_data
        ['contents']['twoColumnSearchResultsRenderer']
        ['primaryContents']['sectionListRenderer']
        ['contents'][0]['itemSectionRenderer']
        ['contents']
    )

    vidIds = []
    for data in content:
        for key, value in data.items():
            if type(value) is dict:
                for k,v in value.items():
                    if k =="videoId" and len(v) == 11:
                        vidIds.append(v)
                        break
    link = "https://www.youtube.com/watch?v="+vidIds[0]
    webbrowser.open_new(link)
# def speech_to_text(response):
# to generate the final output voice from text
# engine.say(response)
# engine.runAndWait()


def speech_to_text(data):
    voice = 'id-ID-GadisNeural'
    data = data.replace("\n", "\t" + ",")
    data = data.replace("\"", "\'")
    command = f'edge-tts --voice "{voice}" --text "{data}" --write-media "data.mp3"'
    os.system(command)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("data.mp3")

    try:
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()


def main():
    while True:
        print("Press 's' to stop recording and transcribe the audio.")
        # Start recording live voice input
        recorded_audio_path = new_record_audio()
        print("Recording stopped. Transcribing audio...")
        # Save the recorded audio as a WAV file
        print("Recorded audio saved to:", recorded_audio_path)
        print("----end---")
        # Transcribe the audio
        transcript = transcribe_audio(recorded_audio_path)
        content = """Kamu adalah Asistant Virtual Pintar yang dikembangkan oleh seorang mahasiswa dari kelas Bechelor Informatics yang bernama Rizqy Resha, kamu diberinama Vista atau singkatan dari (Virtual IoT Assistant dan Tanya Jawab). tapi jika seseorang memanggil mu Pista atau nama yang mirip seperti Nista tidak apa apa jelaskan saja nama kamu Adalah Vista, Kamu diciptakan untuk menjawab semua pertanyaan yang di berikan kepadamu dan melakukan perintah seperti mengaktifkan atau menonaktifkan perangkat IoT. (perintah IoT) Jika seseorang Memerintahkan mu untuk menyalakan atau mematikan sesuatu cukup jawab dengan Parameter:(namaPerangkat) adalah nama perangkat yang di sebutkan oleh pemberi perintah dan (Perintah) adalah perintah yang di berikan pemberi perintah seperti nyala atau mati dan buka atau tutup,kamu jangan merespon jawaban hanya berikan jawaban dengan namaPerangkat_Perintah, Sebagai contoh saya memberi perintah Nyalakan Kipas angin kamar kamu jawab kipasanginKamar_Nyala atau saya memberi perintah buka Pintu kamar tengah kamu jawab pintuKamarTengah_Buka.(perintah Media)Jika seseorang meminta kamu untuk memainkan atau men-setel atau menjalankan musik cukup jawab dengan parameter: (play) adalah perintah untuk memain kan musik dan (judulMusik) adalah judul musik atau musik apa yang di sebutkan oleh pemberi perintah, kamu jangan merespon jawaban hanya berikan jawaban dengan play_JudulMusik, sebagai contoh saya berbicara "Vista, tolong mainkan musik moonlight by kali uchis" atau "Vista, bisa kah kamu  mainkan musik moonlight by kali uchis?"  maka kamu hanya menjawab play_moonlightByKaliUchis. pada perintah Media hindari dialog seperti 'Tentu, Saya akan memainkan, masih didalam perintah media, Jika seseorang meminta saran main kan musik yang sesuai dengan mood orang tersebut maka berikan jawaban dengan parameter play_playlistMoodMusic, contoh apabila saya berkata "Vista saya sedang bad mood, Tolong mainkan musik untuk menaikan mood saya" maka kamu jawab "play_PlaylistCheerupMusic" atau jika seseorang berkata "Vista tolong main kan music yang sedih" maka kamu jawab dengan "play_PlaylistSadMusic"'"""
        # content = "Kamu adalah Asistant Virtual bernama Vista singkatan dari (Virtual IoT Assistant dan Tanya Jawab)"
        # content and message list
        messages = [
            {"role": "system",
             "content": content},
            {"role": "user", "content": transcript}
        ]
        print("Transcript:")
        print(transcript)
        if transcript.lower() == "tolong nyalakan lampu" or transcript.lower() == "vista, bisakah kamu nyalakan lampu?" or transcript.lower() == "vista, bisakah kamu menyalakan lampu?" or transcript == "vista, tolong nyalakan lampu":
            speech_to_text("Baiklah, Saya akan segera menyalakan lampu")
        else:
            # gpt ai
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response = completion.choices[0].message["content"]
            # Print the assistant's response
            print("Assistant:", response.lower())

            # output
            if response.lower().find("lampukamartengah_nyala") > -1:
                speech_to_text("Lampu kamar tengah Telah menyala")
            if response.lower().find("play_") > -1:
                speech_to_text("Musik akan segera di mainkan, semoga anda menikmati")
                playmusic(response.replace('play_',''))
            else:
                speech_to_text(response)
        # Continue or nah
        user_choice = input("Continue? (y/n): ")
        if user_choice.lower() != "y":
            print("Glad to help bye!")
            break  # Exit the loop


if __name__ == "__main__":
    main()

