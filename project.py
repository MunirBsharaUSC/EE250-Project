import pyaudio
import numpy as np
from pydub import AudioSegment
import wave

import requests


# setting constants for sampling from microphone
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 10000
SECONDS = 0.25
MAX_FRQ = 2250

offload_url = 'http://172.20.10.12:5000' 

# array of frequency generated from the base pitch of notes
FREQUENCIES = [[16.35 * 2**x for x in range (7)],
               [17.32 * 2**x for x in range (7)],
               [18.35 * 2**x for x in range (7)],
               [19.45 * 2**x for x in range (7)],
               [20.60 * 2**x for x in range (7)],
               [21.83 * 2**x for x in range (7)],
               [23.12 * 2**x for x in range (7)],
               [24.50 * 2**x for x in range (7)],
               [25.96 * 2**x for x in range (7)],
               [27.50 * 2**x for x in range (7)],
               [29.14 * 2**x for x in range (7)],
               [30.87 * 2**x for x in range (7)]]

NOTE = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]

def get_max_frq(frq, fft) -> float:
    """Returns the frequency with the highest amplitude in the given FFT array.

    Works by iterating through the FFT array and comparing the current amplitude
    to the maximum amplitude. If the current amplitude is greater than the
    maximum amplitude, the current frequency is saved as the maximum frequency
    and the current amplitude is saved as the maximum amplitude.
    
    Args:
        frq (Iterable[float]): The frequency array (x-axis in plots)
        fft (Iterable[float]): The FFT array (y-axis in plots)

    Returns:
        float: The frequency with the highest amplitude in the given FFT array
    """
    max_frq = 0
    max_fft = 0
    for idx in range(len(fft)):
        if abs(fft[idx]) > max_fft:
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return max_frq

def sample_sound() -> float:
    # sampling input from microphone
    mic = pyaudio.PyAudio()
    stream = mic.open(format = FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    mic.terminate()
   
    # Output to audio file.

    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(mic.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

############################# Getting audio from microphone output #############################
    audio = AudioSegment.from_wav("output.wav")
    sample_count = audio.frame_count()
    sample_rate = audio.frame_rate

    samples = audio.get_array_of_samples()
    period = 1/sample_rate                  # the period of each sample
    duration = sample_count/sample_rate     # length of full audio in seconds
    time = np.arange(0, duration, period)   # generate a array of time values from 0 to [duration] with step of [period]

############################# Performing Fourier Transform on sample #############################
    n = duration * sample_rate                           # n is the number of elements in the slice
    k = np.arange(n)                                     # k is an array from 0 to [n] with a step of 1
    frq = k/duration                                     # generate the frequencies by dividing every element of k by slice_duration

    sample_fft = np.fft.fft(samples)/n   # perform the fourier transform on the sample_slice and normalize by dividing by n

    max_frq_idx = int(MAX_FRQ*duration)       # get the index of the maximum frequency (2000)
    frq = frq[range(max_frq_idx)]                   # truncate the frequency array so it goes from 0 to 2000 Hz
    sample_fft = sample_fft[range(max_frq_idx)]     # truncate the sample slice fft array so it goes from 0 to 2000 Hz

    return get_max_frq(frq, sample_fft)

def get_note_from_frq(frq: float) -> str:
    
    minimum = 9999          # initializing min to a large value
    index = -1
    for i in range(12):
        temp = np.min(np.abs(np.array(FREQUENCIES[i]) - frq))
        if (temp < minimum):
            minimum = temp
            index = i
    return NOTE[index]

def main():
    print("Sampling Sound...")
    while(True):
        pitch = sample_sound()
        note = get_note_from_frq(pitch)

        data= f"{pitch:0,.2f},{note}"
        requests.post(f'{offload_url}/display', json = data)

        # print(data)

if __name__ == "__main__":
    main()