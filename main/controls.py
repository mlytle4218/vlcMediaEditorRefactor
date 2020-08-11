#!/env/bin/env python3
import logging

#local imports
from main import config
from main import vlc


class Controls():
    def __init__(self, duration, mediaFile):
        """
        Class for separating the playback and controls for it.

        Parameters
        ----------
        duration - the duration of the song in milliseconds
        mediaFile - the file information of the media to play back
        """
        self.duration = duration
        self.jumpSpanLong = config.jump_span_long/duration
        self.jumpSpanShort = config.jump_span_short/duration

        self.preview = config.preview_time/duration

        self.mediaFile = mediaFile


        self.VLC = vlc
        self.instance = self.VLC.Instance(('--no-video'))
        self.song = self.instance.media_player_new()
        self.media = self.instance.media_new(self.mediaFile)
        self.song.set_media(self.media)

        self.song.play()

    def pausePlay(self):
        state = self.song.get_state()
        # playing
        if state == 3:
            self.song.pause()
        # paused
        elif state == 4:
            self.song.play()
        # stopped
        elif state == 5:
            self.song.play()

    def getTime(self):
        """
        Method to get the current time of the media in milliseconds - this seems
        to be calculated and not reliable for tracking position

        Parameters
        ----------
        None

        Returns
        -------
        int 
            current time in miiliseconds
        """
        return self.song.get_time()

    def getPos(self):
        """
        Method to get the current poistion of the media in long int from 0 to 1

        Parameters
        ----------
        None

        Returns
        -------
        int 
            current position in long decimal
        """
        return self.song.get_position()

    def longJumpForward(self):
        """
        Method to jump the media playback forward by a set amount which is 
        determined by the config

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        logging.debug('jump forward')
        self.changePosition(self.jumpSpanLong)

    def longJumpBackward(self):
        """
        Method to jump the media playback backward by a set amount which is 
        determined by the config

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.changePosition(-self.jumpSpanLong)
    
    def changePosition(self, offSet):
        """
        Method to change the current play position of the media. 

        Parameters
        ----------
        offSet - float - the ammount to change the playback position. A positive
        amount will move it forward and anegative amount will move it back. 

        If the playback is found to be in a stopped state, it will restart the 
        playback with the assumption it was at the end of the file.

        Returns
        -------
        None
        """
        currentPos = self.song.get_position()

        # if song is in a stopped state
        if self.song.get_state() == 6:
            if (currentPos + offSet) < 1:
                self.song = self.instance.media_player_new()
                self.media = self.instance.media_new(self.mediaFile)
                self.song.set_media(self.media)
                self.song.play()
                self.song.set_position(currentPos + offSet)
        else:
            # if the offset doesn't push past the outer bounds of the media
            # play back, continue
            if 0 < (currentPos + offSet) < 1:
                self.song.set_position(currentPos + offSet)

            # offSet tries to go past beginning of file
            elif (currentPos + offSet) < 0:
                self.song.set_position(0)

            # offSet tries to go past end of file
            elif (currentPos + offSet) >  self.duration:
                # self.song.set_position(self.duration)
                pass

            # # offSet is in valid region
            # else:
            #     self.song.set_position(currentPos + offSet)


    