#!/usr/bin/env python3 
import time
import threading
import logging

# local imports
from main import sounds


class WorkerThread(threading.Thread):
    """
    A worker thread that polls the vlc api for current position and calls options as necessary

    Ask the thread to stop by calling its join() method.
    """

    def __init__(self, song):
        super(WorkerThread, self).__init__()
        # song here is actually pulling in the whole main object to access it. 
        # not a great way to do it...
        self.song = song
        self.stoprequest = threading.Event()
        self.last = 0

        self.current_position = 0
        self.difference = 0.0025
        logging.debug(self.song.preview)
        # self.difference = 0.005

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        # difference - this is a 'magic' number to give leaway to testing to each
        # mark relative to the current time. because there could be variation 
        # between the polled time from vlc and the current mark, it needs a 
        # cushion to test against. This needs to be converted to a algorith 
        # relative to the length of the file.

        while not self.stoprequest.isSet():
            self.current_position = self.song.con.getPos()
            if abs(self.current_position - self.last) > 0:
                try:
                    # self.song.print_to_screen(str(self.current_position))
                    # pass
                    for itr,each in enumerate(self.song.state.marks):
                        if abs(self.current_position - self.last) != 0:
                            # If the start point falls in the range of
                            if self.last < (each.start + self.song.preview) < self.current_position:
                                logging.debug("print edit to screen at {}".format(self.current_position))
                                self.song.print_to_screen("Edit {}".format(itr+1))

                            # if the start point falls in the range of last and current_position
                            # then jump to the end
                            if self.last < each.start < self.current_position:
                                logging.debug("start jump to screen at {}".format(self.current_position))
                                logging.debug(each.start)
                                self.song.con.song.set_position(each.end)
                                self.song.con.song.pause()
                                time.sleep(1)
                                self.song.con.song.play()

                    #     if abs(self.current_position - self.last) < self.difference: 
                    #         if self.song.is_editing:
                    #             # self.song.log("{}:{}".format(self.last <= each.end, each.end <= self.current_position))
                    #             # res = self.last - self.difference <= each.end <= self.current_position + self.difference
                    #             # if res:
                    #             #     self.song.log(res)
                    #             try:
                    #                 if self.last <= each.start <= self.current_position:
                    #                     self.song.print_to_screen('Block {} start'.format(itr + 1))
                    #                     if each.start != 0:
                    #                         self.song.startSound()
                    #                 if self.last <= each.end <= self.current_position:
                    #                     self.song.print_to_screen('Block {} end'.format(itr + 1))
                    #                     self.song.endSound()
                    #             except Exception as ex:
                    #                 self.song.log(ex)
                    #         else:
                    #             if self.last <= each.start <= self.current_position:
                    #                 # self.song.log("each.start {}".format(each.start))
                    #                 # keep the marks iterator up to date on the location in the file
                    #                 self.song.markItr = itr
                    #                 self.song.updateIters()
                    #                 self.song.song.set_position(each.end)
                    #                 self.song.print_to_screen('Block {}'.format(itr + 1))
                    #                 self.song.song.pause()
                    #                 time.sleep(1)
                    #                 self.song.song.play()

                    
                    
                except Exception as ex:
                    logging.warning(ex)
                self.last = self.current_position

    # used to shut down the worker thread
    def join(self, timeout=None):
        logging.info('WorkerThread stopped')
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)