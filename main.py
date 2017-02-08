import sys
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


sys.stdout.write("initializing..."); sys.stdout.flush()
rec = a2t.Recognizer()
with a2t.Microphone(mic_index) as mic:
    rec.dynamic_energy_adjustment_ratio = 2

    try:
        rec.listen(mic, timeout=1, phrase_time_limit=3)
    except a2t.WaitTimeoutError:
        pass    # nothing detected

    print("done.")

    iteration = 0
    while True:
        text = None
        wake = None
        try:
            if iteration % 5 == 0:
                sys.stdout.write("adjusting for noise..."); sys.stdout.flush()
                rec.adjust_for_ambient_noise(mic, 5)
                print("done.")
            sys.stdout.write("listening... "); sys.stdout.flush()
            sample = rec.listen(mic, timeout=2, phrase_time_limit=3)
            sys.stdout.write("recognizing... ")
            text = rec.recognize_sphinx(sample)
            wake = rec.recognize_sphinx(sample,
                                        keyword_entries=[("computer", 0.5)])
        except a2t.WaitTimeoutError:
            pass    # nothing detected
        except a2t.UnknownValueError:
            pass    # wake word not recognized
            # print("audio_handler: sample value error")
        except a2t.RequestError as e:
            print("audio_handler: recognition error - {0}".format(e))
        except Exception as e:
            print("audio_handler: unknown error - {0}".format(e))
        print("wake: {:20} text: {}".format(wake or "", text or ""))
        iteration = iteration + 1
