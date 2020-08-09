#!/usr/env python3
import os
import subprocess
import json
import shutil
import pickle
import logging
from pathlib import Path

#local imports
from main import state

class MediaFileActions():
    """
    Class to localize the file I/O operations

    Parameters
    ----------
    inputFile - the media file.
    """
    def __init__(self, inputFile):
        logging.info('FileActions init')
        logging.info(Path(inputFile).absolute())
        self.inputFile = inputFile
        self.stateFile = self.getStateFileName(self.inputFile)
        self.backup = self.backUpFileIfNotAlreadyBackedUp(self.inputFile)
        self.sample, self.bit = self.getRates(self.inputFile)
        self.state = state.State(self.stateFile)
        self.duration = self.getFileDuration()

    def getRates(self, inputFile):
        """
        returns the sample and bit rate of the inputFile

        Parameters
        ----------
        inputFile: string
            The file passed to program

        Returns
        -------
        int
            sample rate as int

        int
            bit rate as int
        """
        sample_rate = None
        bit_rate = None
        cmd = ['ffprobe', '-v', 'quiet', '-print_format',
               'json', '-show_streams', self.inputFile]
        result = json.loads(
            subprocess.check_output(cmd).decode('utf-8')
        )
        for stream in result['streams']:
            if stream['codec_type'] == "audio":
                bit_rate = int(stream['bit_rate'])
                sample_rate = int(stream['sample_rate'])
        return sample_rate, bit_rate

    def getStateFileName(self, inputFile):
        """
        Takes the object inputFile and detremines a state filename from that and
        places it in self.stateFile

        Parameters
        ----------
        inputFile: string
            The file passed to program

        Returns
        -------
        string
            The name and location of where the state fiel should be if it exists
        """
        file_path = os.path.dirname(os.path.realpath(inputFile))
        file_name= os.path.splitext(
            os.path.basename(inputFile)
        )[0]
        return os.path.join(
                file_path,
                file_name + ".state"
            )

    def backUpFileIfNotAlreadyBackedUp(self, inputFile):
        """
        checks if a backupfile already exists and makes one if its not there

        Parameters
        ----------
        inputFile: string
            The file passed to program

        Returns
        -------
        boolean
            True if it created a backup file
        """
        new_file = inputFile + "~"
        if not os.path.exists(new_file):
            shutil.copyfile(inputFile, new_file)
        return new_file

    def getFileDuration(self):
        """
        Gets the length of the original file

        Parameters
        ----------
        inputFile - string - the path and file name of the file

        Returns
        -------
        int
            the length of the media file in milliseconds
        """
        time = 0
        command = ['ffmpeg', '-i', self.inputFile, '-f', 'null', '-']
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = result.stdout.decode('utf-8').splitlines()
        for line in lines:
            for word in line.split():
                if word.startswith('time='):
                    time_temp = word.split("=")[1].split(":")
                    time = int(time_temp[0]) * 3600 + int(time_temp[1]
                                                          )*60 + round(float(time_temp[2]))
        return time * 1000