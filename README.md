# Command Line Video editor for visually impaired

This is for editing audio and video by audio only. It relies on videoLan to play the audio/video. It tracks the *edits* by creating blocks to be removed. When finished, it passes that information on to ffmpeg with timecode blocks that are be be kept. (The opposite of the editing process.) It re-encodes the file with only the wanted sections of the file kept.

There are two versions of operability
./player.py - shows markers for the beginning and ending of marks 
./player2.py - jumps from the the beginning of a block to the end of the block making it sound like a removed block is gone


## Requirements
- [Python](https://www.python.org/) 3.6 or later.
- [VideoLan](https://www.videolan.org/index.html) video player  
- [ffmpeg](https://www.ffmpeg.org/)  
- [ncurses](https://linux.die.net/man/3/ncurses)
