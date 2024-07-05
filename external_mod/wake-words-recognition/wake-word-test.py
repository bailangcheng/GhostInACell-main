# Checking OS platform
from sys import platform

# Script configuration
import config

# Wake word detection
import pvporcupine
from pvrecorder import PvRecorder

# OSC
from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder

# Configure Porcupine keyword model paths based on platform
access_key = config.access_key

# List the model and keyword file paths separately
keyword_model_mac = 'porcupine_params_ja.pv'
keyword_hi_mac = 'hi_neurons_ja_mac_v3_0_0.ppn'
keyword_hello_mac = 'hello_neurons_ja_mac_v3_0_0.ppn'  # Add the new keyword file for mac
keyword_model_windows = 'porcupine_params_ja.pv'
keyword_hi_windows = 'hi_neurons_ja_windows_v3_0_0.ppn'
keyword_hello_windows = 'hello_neurons_ja_windows_v3_0_0.ppn' # Add the new keyword file for windows

if platform == 'win32':
    keyword_model_path = keyword_model_windows
    keyword_paths = [keyword_hi_windows, keyword_hello_windows]  # Include both keywords
elif platform == 'darwin':
    keyword_model_path = keyword_model_mac
    keyword_paths = [keyword_hi_mac, keyword_hello_mac]  # Include both keywords
else:
    print('Operating system not supported. Run this program on a Windows or Mac machine')
    exit()

# Define wake words as a list 
keywords = ['ハイ ニューロン', 'ハロー ニューロン']  

# Create Porcupine instance with multiple keywords
porcupine = pvporcupine.create(
    access_key=access_key,
    model_path=keyword_model_path,
    keyword_paths=keyword_paths,
    keywords=keywords
)
# Show available audio devices
print("Available audio devices:")
for i, device in enumerate(PvRecorder.get_available_devices()):
    print(f"Device {i}: {device}")

# Setup OSC client
IP = '127.0.0.1'
PORT = 10000
client = udp_client.SimpleUDPClient(IP, PORT)

# Initialize voice recorder with device_index=2
try:
    device_index = 0  # Adjust according to the device you want to use
    recorder = PvRecorder(device_index=device_index, frame_length=porcupine.frame_length)
    recorder.start()
    print(f'Listening ... Say either of "{keywords[0]}" or "{keywords[1]}" to trigger (press Ctrl+C to exit)') 

    # Listen for wake word and send OSC message
    while True:
        pcm = recorder.read()
        result = porcupine.process(pcm)
        if result >= 0:
            print(f"Wake Word detected: {keywords[result]}")

            # Send OSC message
            builder = OscMessageBuilder(address="/wake_neurons")
            builder.add_arg(result)
            msg = builder.build()
            client.send(msg)

except KeyboardInterrupt:
    print('Stopping ...')

finally:
    if 'recorder' in locals():
        recorder.delete()
    if 'porcupine' in locals():
        porcupine.delete()
