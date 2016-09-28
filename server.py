
# Echo server program
import socket
import pyaudio
import wave
import time
import audiere
import thread

def playaudio(audio_array):
    ds = audiere.open_device()
    os = ds.open_array(audio_array, 44100)
    os.play()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "server_output.wav"
WIDTH = 2
BUFFER_SIZE = 32;

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)


HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
data = conn.recv(1024)

while data != '':
    stream.write(data)
    data = conn.recv(1024)
    if len(frames) <= 32:
        frames.append(data)
    else:
        playback = ''.join(frames)
        thread.start_new_thread( playaudio, (playback,  ) )
        frames = []



stream.stop_stream()
stream.close()
p.terminate()
conn.close()
