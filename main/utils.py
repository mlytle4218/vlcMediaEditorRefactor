#!/usr/bin/env python3




class Utils():
    def __init__(self):
        pass

    def millisecondsToTimeStamp(self, milliseconds):
        """
        Method to create a time stamp for a number of milliseconds

        Parameters
        ----------
        milliseconds - int - milliseconds

        Returns
        -------
        string - the milliseconds in the form of hours, minutes and seconds
        """
        milliseconds = int(milliseconds/1000)
        minutes = int((milliseconds / 60) % 60)
        hours = int((milliseconds / (60*60)) % 3600)
        sec = int(milliseconds - (minutes * 60) - (hours * 60 *60))
        time = ""
        if hours >= 1:
            time = "{} hours ".format(hours)
        if minutes >= 1:
            time += "{} minutes ".format(minutes)
        if sec >= 1:
            time  += "{} seconds".format(sec)
        return time


    def timeStamp(self,duration,current):
        """
        Method to create a time stamp for the current position in the media.

        Parameters
        ----------
        duration - int - length of the media in seconds
        current - float - the current position in the media playback

        Returns
        -------
        string - the hours, minutes and seconds of the curretn playback position
        """
        out = duration * current
        millis = int(out)
        if millis == 0:
            return '0'
        seconds = round((millis/1000) % 60, 3)
        minutes = (millis/(1000*60)) % 60
        minutes = int(minutes)
        hours = int((millis/(1000*60*60)) % 24)
        time = ""
        if hours >= 1:
            time = "{} hours ".format(hours)
        if minutes >= 1:
            time += "{} minutes ".format(minutes)
        if seconds >= 1:
            time  += "{} seconds".format(seconds)
        return time


if __name__ == "__main__":
    utils = Utils()
    result = utils.millisecondsToTimeStamp(14643)
    print(result)
    result = utils.millisecondsToTimeStamp(268)
    print(result)