# EE250-Project
LINK TO DEMO: 
    https://youtu.be/P0upNeKgBWw 

TEAM MEMBERS:
    Hongyu Zhao
    Munir Bshara

LIBRARIES:
    pyaudio
    numpy
    pydub
    wave
    requests
    flask
    grovepi

Instructions:

    First get the project.py file onto your laptop (make sure it has a microphone). This will be the client. Then, get the serverNOTES.py file onto the Raspberry PI. This will be the server.

    Make sure that the grovepi shield is attached to the pi and that the lcd is attached to the I2C port on the shield. 

    First run the serverNotes.py file on the pi and then run the project.py file on your laptop with python3 (it must be done in this order). The LCD should now update to display the frequency and corresponding note. Then, to stop either one, press CTRL + C.

NOTES:

    You may have troubles installing pyaudio with pip on the VM. It's much easier to install it locally on Windows.

    Since the project.py file accesses your microphone to sample sound, your laptop must have a microphone. Additionally, your laptop may have audio enhancements such as noise filtering/cancellation on the microphone which may hinder it's ability to detect a sound coming from an instrumnet. For the best results, turn off any software enhancements that may be on the microphone.

    There will be an "output.wav" file created in the directory. This file is just the sample that is taken that an FFT is performed on.