import mpv

import os
import sys
import time
import pathlib
import datetime 
from tkinter import filedialog

#
# Handle global values
#

DEBUG_MODE = os.environ.get("DEBUG_MODE", None) != None

OUTPUT_FILE = os.environ.get("OUTPUT_FILE", pathlib.Path.home() / ".mpv-title.txt")

if not OUTPUT_FILE:
    print("OUTPUT_FILE not defined...", file=sys.stderr)
    sys.exit(1)

#
# Helper functions
#

now = lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def debugPrint(text):
    if DEBUG_MODE:
        print("[DEBUG]", now(), text, file=sys.stderr, flush=True)

def writeFile(text):
    try:
        OUTPUT_FD = open(OUTPUT_FILE, "w")
        OUTPUT_FD.write(text)
        OUTPUT_FD.close()
    except Exception as e:
        print(f"error: {e}, {type(e)}", file=sys.stderr)
        sys.exit(1)

def getMusicFolder():
    return filedialog.askdirectory()

#
# Player singleton instance setup
#

PLAYER = mpv.MPV(
    player_operation_mode='pseudo-gui',
    script_opts='osc-layout=box,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=3',
    input_default_bindings=True,
    input_vo_keyboard=True,
    osc=True,
)

# PLAYER.fullscreen = True
PLAYER.loop_playlist = "inf"

#
# Interrupts
#

@PLAYER.property_observer("media-title")
def media_title_observer(_name, value):
    artist = None
    if PLAYER.metadata:
        artist = PLAYER.metadata.get("artist", None)

    title = None
    if value:
        title = value

    output = f"artist: {artist}, title: {title}"
    writeFile(output)
    debugPrint(output)

#
# Main logic
#

if __name__ == "__main__":
    try:
        folder = getMusicFolder()
        PLAYER.loadlist(folder)
        debugPrint(f"loading folder: {folder}")
    except Exception as e:
        print(f"something failed while loading the music folder... error: {e}")
        sys.exit(1)

    # shuffle the songs and set the player to play the first in the queue
    PLAYER.command("playlist-shuffle")
    PLAYER.command("playlist-play-index", 0)

    try:
        # keep the process running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("closing mpv...")
        PLAYER.terminate()
    except Exception as e:
        print(f"error: {e}, {type(e)}", file=sys.stderr)
        sys.exit(1)
