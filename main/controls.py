#!/env/bin/env python3
import logging
import time

#local imports
from main import config
from main import vlc
from main import utils


class Controls():
    def __init__(self, state, print_func, mediaFile):
        """
        Class for separating the playback and controls for it.

        Parameters
        ----------
        duration - the duration of the song in milliseconds
        mediaFile - the file information of the media to play back
        """
        self.state = state
        self.print_func = print_func
        self.duration = self.state.duration
        self.jumpSpanLong = config.jump_span_long/self.duration
        self.jumpSpanShort = config.jump_span_short/self.duration

        self.preview = config.preview_offset/self.duration

        self.mediaFile = mediaFile

        self.utils = utils.Utils()        

        self.VLC = vlc
        self.instance = self.VLC.Instance(('--no-video'))
        self.song = self.instance.media_player_new()
        self.media = self.instance.media_new(self.mediaFile)
        self.song.set_media(self.media)
        self.song.reset = 0

        self.song.play()

    def jumpToNextEdit(self):
        nextMark = self.state.playBackNext()
        logging.debug(nextMark.start + self.preview)
        self.song.set_position(nextMark.start + self.preview)
        pass

    def getComputerTime(self):
        """
        Method to get the current machine time. 
        Parameters
        ----------
        None

        Returns
        -------
        int 
            current machine time in seconds.
        """
        return int(round(time.time() *1000))

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
        logging.debug('jump backward')
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

        # if song is in a stopped state
        if self.song.get_state() == 6:
            if offSet < 0:
                self.song = self.instance.media_player_new()
                self.media = self.instance.media_new(self.mediaFile)
                self.song.set_media(self.media)
                self.song.play()
                self.song.pause()
                self.song.set_position(1-abs(offSet))
                self.song.play()
                self.song.reset = self.getComputerTime()
            else:
                self.print_func("End of File.")
        else:
            currentPos = self.song.get_position()
            # if the offset doesn't push past the outer bounds of the media
            # play back, continue
            if 0 < (currentPos + offSet) < 1:
                newPos = currentPos + offSet
                # for itr,each in enumerate(self.state.marks):
                for each in self.state.marks:
                    if each.start < newPos < each.end:
                        if offSet < 0:
                            newPos = each.start + offSet
                            # self.print_func("Edit {}".format(itr+1))        
                        else:
                            newPos = each.end + offSet
                            # self.print_func("Edit {}".format(itr+1))        

                        # if offSet < 0:
                        #     newPos = each[1].start + (offSet + (currentPos - each[1].end ) ) 
                        # else:
                        #     newPos = each[1].end + ( offSet - (each[1].start - currentPos))
                    
                    
                    self.song.set_position(newPos)

            # offSet tries to go past beginning of file
            # stupid little hack - needs this because the get_position method is no
            # returning anything and being interpreted as 0 sending the song back to
            # the beginning
            elif (currentPos + offSet) < 0 and abs(self.song.reset - self.getComputerTime()) > 1000:
                self.song.set_position(0)

            # offSet tries to go past end of file
            elif (currentPos + offSet) >  self.duration:
                self.print_func("End of File.")

            # # offSet is in valid region
            # else:
            #     self.song.set_position(currentPos + offSet)

    def jumpSpecificTime(self, input_func, print_func):
        """
        Method that asks the user which direction and then how far the user wants
        to move through the media file and then advances that far.

        Parameters
        ----------
        input_func - function - a function that can print to the screen and 
        accept the input from the user
        print_func - fucntion - a function to only print to the screen

        Returns
        -------
        None
        """
        self.song.pause()
        direction = input_func('forward?', 1)
        reverse = 1
        if direction.decode().lower() == "b":
            self.song.set_position(0)
        elif direction.decode().lower() == "e":
            self.song.set_position(1 - (self.jumpSpanLong))
        elif direction.decode() == "-" or direction.decode() == "":
            if direction.decode() == "-":
                reverse = -1
            hours = self.getNumFromInput("hours?", input_func, print_func) * 60 *60
            minutes = self.getNumFromInput("minutes?", input_func, print_func) *60
            seconds = self.getNumFromInput("seconds?", input_func, print_func) 
            seconds = (seconds + minutes + hours) * reverse
            seconds *= 1000

            if 0 < abs(seconds) < self.duration:
                self.song.set_position(self.getPos() + seconds/self.duration)
            else:
                time = self.utils.millisecondsToTimeStamp(abs(seconds))
                print_func("{}is beyond the confines of the media.".format(time))
        else :
            print_func("{} is not a valid option".format(direction.decode()))
        self.song.play()

    def getNumFromInput(self, prompt, input_func, print_func):
        """
        Method to get a number from the user. Hard coded to only accept the first
        two numbers. It error checks the input.

        Parameters
        ----------
        prompt - string - what should printed to screen to make request of user
        input_func - function - a function that can print to the screen and 
        accept the input from the user
        print_func - fucntion - a function to only print to the screen

        Returns
        -------
        int - the number as an integer.
        """
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



    

    