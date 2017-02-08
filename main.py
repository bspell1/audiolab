import time

import pyaudio
import speech_recognition as a2t

# find the desired microphone or the first input in the list
mic_index = -1
spk_index = -1
audio = pyaudio.PyAudio()
for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)
    print('device:', info['name'])
    if (info['maxInputChannels'] > 0):
        if (info['name'] == 'USB audio CODEC' or mic_index == -1):
            mic_index = i
    if (info['maxOutputChannels'] > 0 and spk_index == -1):
        spk_index = i


if spk_index != -1:
    print("microphone:")
    print(audio.get_device_info_by_index(mic_index))
else:
    print("microphone not found")
print()
if spk_index != -1:
    print("speaker:")
    print(audio.get_device_info_by_index(spk_index))
else:
    print("speaker not found")
print()


def ambient_handler(rec, mic):
    while True:
        try:
            rec.adjust_for_ambient_noise(mic, 5)
        except Exception as e:
            print("ambient_handler: unknown error - {0}".format(e))


def audio_handler(rec, sample):
    text = None
    wake = None
    try:
        text = rec.recognize_sphinx(sample)
        wake = rec.recognize_sphinx(sample, keyword_entries=[("computer", .5)])
    except a2t.UnknownValueError:
        pass    # wake word not recognized
        # print("audio_handler: sample value error")
    except a2t.RequestError as e:
        print("audio_handler: recognition error - {0}".format(e))
    except Exception as e:
        print("audio_handler: unknown error - {0}".format(e))
    print("wake: {:20} text: {}".format(wake or "", text or ""))


rec = a2t.Recognizer()
mic = a2t.Microphone(mic_index)
listening = False

rec.dynamic_energy_adjustment_ratio = 2
rec.listen_in_background(mic, audio_handler, 3)

time.sleep(5)
while True:
    rec.adjust_for_ambient_noise(mic, 5)
    time.sleep(30)
