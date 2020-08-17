#!/env/bin/env python3
import logging
import time

#local imports
from main import config
from main import vlc
from main import utils


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

        self.utils = utils.Utils()        

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


    def jumpSpecificTime(self, input_func, print_func):
        self.song.pause()
        forward_input = input_func('forward?',1)
        if forward_input.decode() == "b":
            self.song.set_position(0)
        elif forward_input.decode() == "e":
            self.song.set_position(1)
        else:
            reverse = 1
            if forward_input.decode() == "-":
                reverse = -1

            hours = self.getNumFromInput('hours?', input_func, print_func)
            minutes = self.getNumFromInput('minutes?', input_func, print_func)
            seconds = self.getNumFromInput('seconds?', input_func, print_func)
            seconds = seconds + minutes * 60 + hours * 60 * 60 * reverse

            

            if 0 < abs(seconds) < self.duration :
                self.song.set_position(self.duration / seconds)
            else:
                print_func(self.utils.timeStamp(self.duration, seconds))
        self.song.play()

    def getNumFromInput(self, prompt, input_func, print_func):
        while True:
            result = input_func(prompt, 2)
            if result.decode() == '':
                return 0
            try:
                return int(result)
            except ValueError as ve:
                print_func("{} is not a valid option".format(result))
                time.sleep(2)
                logging.warning("Error from {}".format(prompt))
                logging.warning(ve)



    

    