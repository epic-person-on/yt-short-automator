# Import everything
import subprocess
import random
import os
import google.generativeai as genai
from tiktokvoice import tts
import moviepy as mp
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid

# Ask for video info
title = input("\nEnter the name of the video >  ")
option = input('Do you want AI to generate content? (yes/no) >  ')

if option == 'yes':
    # Generate content using OpenAI API
    theme = input("\nEnter the theme of the video >  ")

    key='Placeholder'

    genai.configure(api_key=key)


    prompt=f"generate a very interesting text only no formating or markdown video script start by saying a hook for example 'multiple shocking facts that will shock you' followed by 2 - 4 short facts in the form of sentances that tell about: {theme}",
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(prompt)


    print(response.text)

    yes_no = input('\nIs this fine? (yes/no) >  ')
    if yes_no == 'yes':
        content = response.text
    else:
        content = input('\nEnter >  ')
else:
    content = input('\nEnter the content of the video >  ')

# Create the directory
if os.path.exists('generated') == False:
    os.mkdir('generated')

# Generate speech for the video
tts(content,'en_male_funny','generated/speech.mp3',play_sound=False)

gp = random.choice(["1", "2", "3"])
ms = str(random.randint(1,5))
start_point = random.randint(1, 480)
audio_clip = AudioFileClip("generated/speech.mp3")

if (audio_clip.duration + 1.3 > 58):
    print('\nSpeech too long!\n' + str(audio_clip.duration) + ' seconds\n' + str(audio_clip.duration + 1.3) + ' total')
    exit()

print('\n')

### VIDEO EDITING ###
audio_background = AudioFileClip('Music/'+ ms +'.mp3').subclip(0, audio_clip.duration + 1.3).fx(afx.volumex, 0.3)
composite = CompositeAudioClip([audio_clip,audio_background])
# Trim a random part of minecraft gameplay and slap audio on it
video_clip = VideoFileClip("gameplay/gameplay_" + gp + ".mp4").subclip(start_point, start_point + audio_clip.duration + 1.3)
final_clip = video_clip.set_audio(composite)

# Resize the video to 9:16 ratio
w, h = final_clip.size
target_ratio = 1080 / 1920
current_ratio = w / h

if current_ratio > target_ratio:
    # The video is wider than the desired aspect ratio, crop the width
    new_width = int(h * target_ratio)
    x_center = w / 2
    y_center = h / 2
    final_clip = crop_vid.crop(final_clip, width=new_width, height=h, x_center=x_center, y_center=y_center)
else:
    # The video is taller than the desired aspect ratio, crop the height
    new_height = int(w / target_ratio)
    x_center = w / 2
    y_center = h / 2
    final_clip = crop_vid.crop(final_clip, width=w, height=new_height, x_center=x_center, y_center=y_center)

# Write the final video
final_clip.write_videofile("generated/" + title + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
