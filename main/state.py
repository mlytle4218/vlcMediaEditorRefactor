#!/usr/bin/env python3
import pickle
import logging

# local imports
from main import mark


class State():
    def __init__(self, stateFile):
        self.stateFile = stateFile
        self.marks = []
        self.currentMark = None
        self.duration = 0
        self.playBackIterator = 0
        self.workerThreadIterator = 0

    def setDuration(self, duration):
        self.duration = duration
    
    def getDuration(self):
        return self.duration

    def playBackNext(self):
        """
        Iterates through Marks in list. Will start at beginning if reaches the 
        end.

        Parameters
        ----------
        None

        Returns
        -------
        Mark
            If there is a mark available

        None
            If there is not
        """

        if len(self.marks) > 0:
            try:
                m = self.marks[self.playBackIterator +1]
                self.playBackIterator += 1
                return m
            except (ValueError, IndexError):
                m = self.marks[0]
                self.playBackIterator = 0
                return m
        else:
            return None

    def workerThreadNext(self):
        """
        Iterator for the worker thread. Moves through list once and stops.

        Parameters
        ----------
        None

        Returns
        -------
        Mark
            Return mark if it has not reached the end of the list

        None
            If it has reached the end of the list or the list is empty
        """
        if len(self.marks) > 0:
            try:
                m = self.marks[self.workerThreadIterator +1]
                self.workerThreadIterator += 1
                return m
            except (ValueError, IndexError):
                self.workerThreadIterator = 0
                return None
        else:
            return None

    def logState(self):
        """
        quick method to output state data to log
        """
        for m in self.marks:
            logging.info(m)
            
        logging.info(self.duration)

    def addMark(self, mark):
        """
        syntactic sugar to add mark to state
        """
        self.marks.append(mark)

    def removeMark(self, mark):
        for m in self.marks:
            if m == mark:
                self.marks.remove(mark)

    def writeStateInformation(self):
        """
        Method to write the state information to a file named like the original
        with a .state extension

        Parameters
        ----------
        None

        Returns
        -------
        boolean
            True if it wrote to the state file
        """
        try:
            state = open(self.stateFile, 'wb')
            temp = {"marks":self.marks, "duration":self.duration}
            pickle.dump(temp, state)
            return True
        except Exception as ex:
            logging.warning(ex)
            return False

    def readStateInformation(self):
        """
        Method to read the saved information about a file from a file named like
        the original with a .state extension

        Parameters
        ----------
        None

        Returns
        -------
        boolean
            True if it read the state file
        """
        try:
            state = open(self.stateFile, 'rb')
            temp = pickle.load(state)
            self.marks = temp['marks']
            self.duration = temp['duration']
            return True
        except IOError:
            logging.warning("No state file found")
            return False

    def startEditPoint(self, currentPos):
        """
        Create a new edit mark point and save the current position in it.

        Parameters
        ----------
        currentPos - float - The current position in the media playback

        Returns
        -------
        boolean 
            True if created
        """
        if not self.currentMark:
            self.currentMark = mark.Mark(position=currentPos)
            self.addMark(self.currentMark)
            self.updateScreen('Edit point started.')
            logging.debug('New edit point created at {}'.format(currentPos))
            return True

        return False

    def endEditPoint(self, currentPos):
        """
        End an existing edit mark point and save the current position in it.

        Parameters
        ----------
        currentPos - float - The current position in the media playback

        Returns
        -------
        boolean 
            True if there was a edit point created already and it was ended.
        """
        if self.currentMark:
            self.currentMark.end = currentPos
            self.updateScreen('Edit point ended')
            self.currentMark = None
            logging.debug('New edit point ended at {}'.format(currentPos))
            self.writeStateInformation()
            return True
        return False

    def beginningToNowEdit(self, currentPos):
        """
        Create and save an edit mark point from the current start of the file to
        the current posisition.

        Parameters
        ----------
        currentPos - float - The current position in the media playback

        Returns
        -------
        boolean 
            True if successfully created
        """
        pass

    def nowToEndingEdit(self, currentPos):
        """
        Create and save an edit mark point from the current position to the end 
        of the file. 

        Parameters
        ----------
        currentPos - float - The current position in the media playback

        Returns
        -------
        boolean 
            True if successfully created
        """
        pass


    def updateScreen(self, message):
        pass


    def positionToMilliseconds(self, position):
        """
        Method to change vlc's position to milliseconds

        Parameters
        ---------
        position - float - vlc's position number.

        Returns
        -------
        None
        """
        return int(self.duration * position) / 1000 

    def applyEdits(self, inputFile, outputFile):
        """
        Method to create the final command for editing the original file.

        Parameters
        ----------
        inputFile - string - the full path and file name of the media file - in 
        this case it's the backup file.
        outputFile - string - the full path and file name of the media file - in
        this case, it's the original file name. it will be overwritten

        Returns
        -------
        Array
            Strings representing the ffmpeg command with all the info for 
        successful editing. 
        """

        com = ['ffmpeg', '-i', inputFile]
        select = "select='"
        aselect = "aselect='"

        # this reorganizes the marks to represent the blocks between the 'removed'
        # blocks
        last = 0
        for each in self.marks:
            temp = each.end
            each.end = each.start
            each.start = last
            last = temp

        n = mark.Mark()
        n.start = last
        n.end = 1
        self.marks.append(n)

        # filter all the ones where start and end are equal
        # probably not needed any more
        marks = list(
            filter(
                lambda item: item.start != item.end, self.marks
                )
            )

        for i, each in enumerate(marks):
            bit = """between(t,{},{})""".format(
                    self.positionToMilliseconds(each.start),
                    self.positionToMilliseconds(each.end)
                )
            if i != 0:
                select += "+"
                aselect += "+"
            
            select += bit
            aselect += bit

        select += """',setpts=N/FRAME_RATE/TB """
        aselect += """',asetpts=N/SR/TB"""
        com.append('-vf')
        com.append(select)
        com.append('-af')
        com.append(aselect)
        com.append(outputFile)
        # logging.info(com)
        return com