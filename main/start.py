#!/usr/bin/env python3
import curses
import logging

#local files
from main import config
from main import mediaFileActions
from main import state
from main import vlc
from main import controls
from main import workerThread
from main import markControls
from main import mark

class start(object):
    def __init__(self, window, args):
        # this is command that will be passed to ffmpeg to do all the actual 
        # work of editing the file
        command = args[0]

        # media file to be edited
        mediaFile = args[1]

        # verbosity of the logging being determinied
        num_level = getattr(logging, config.log_level)
        logging.basicConfig(filename='player.log',level=num_level)


        logging.info("Loading file: {}".format(mediaFile))
        
        # create the object to do all the file I/O stuff
        fa = mediaFileActions.MediaFileActions(mediaFile)

        # calculate this value now to have available for the thread later
        self.preview = config.preview_offset/fa.duration

        # create a state object that holds and writes all the info about a song
        # and it's edits
        self.state = state.State(fa.stateFile)

        # Try and see if there is already a file saved of the state information
        # If if can't be read, then it has to be created and info added
        if not self.state.readStateInformation():
            self.state.setDuration(fa.duration)
            self.state.writeStateInformation()

        # initialize controls for playback
        self.con = controls.Controls(
            self.state.duration,
            fa.backup
        )
                
        # Start the other thread that watches VLC's playback and calls cues when
        # needed
        self.pollingThread = workerThread.WorkerThread(self)
        self.pollingThread.start()
        
        
        try:
            self.window = window.subwin(0,0)

            # set curses to interpret escape characters 
            self.window.keypad(1)

            # clears the screen
            self.window.clear()
             
            # rewrites the screen
            self.window.refresh()

            # set the curses cursor to invisible
            curses.curs_set(0)

            while True:
                key = window.getch()

                # CONTROLS
                # Quit program
                if key == config.quit_program:
                    self.pollingThread.join()
                    break
                
                # Apply the edits to the media file and exit
                elif key == config.begin_edits:
                    logging.debug(fa.backup)
                    if fa.backup:
                        command.extend(
                            self.state.applyEdits(
                                fa.backup,
                                fa.inputFile
                            )
                        )
                        self.con.pausePlay()
                        self.pollingThread.join()
                        break
                    else:
                        logging.warning('no bakup file')

                #jump forward long
                elif key == config.jump_forward:
                    self.con.longJumpForward()
                
                #jump backward long
                elif key == config.jump_back:
                    self.con.longJumpBackward()

                # pause/start playback
                elif key== config.play_pause:
                    self.con.pausePlay()

                #EDITING
                elif key == config.mark_start_pos:
                    self.state.startEditPoint(self.con.getPos())

                elif key == config.mark_end_pos:
                    self.state.endEditPoint(self.con.getPos())

                #UTILITIES
                elif key == ord('w'):
                    self.state.logState()

                elif key == ord('j'):
                    logging.debug(self.con.getTime())
                    logging.debug(self.con.getPos())



        except KeyboardInterrupt:
            pass


    def print_to_screen(self, output):
        """
        Method that prints the time (formatted) of the current postion

        Parameters
        ----------
        output
            string - what is supposed to printed to screen

        Returns
        -------
        None
        """
        self.window.clear()
        self.window.addstr(0, 0, output)
        self.window.refresh()

        curses.doupdate()

    def dummy(self):
        """
        one-liner

        Deeper description

        Parameters
        ----------
        arg: type
            description

        Returns
        -------
        type
            description
        """