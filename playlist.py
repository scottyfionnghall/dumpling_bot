import os
import random
from dotenv import load_dotenv
load_dotenv()
directory = os.getenv('MUSIC_DIR')
def playlist():
    song_list = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            song_list.append(f)
        random.shuffle(song_list)
    return(song_list)

def playlist_get_dir():
    return(str(directory))