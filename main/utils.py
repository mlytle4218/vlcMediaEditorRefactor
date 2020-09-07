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
        string - the milliseconds in the form of hour, minutes and seconds
        """
        seconds = round((milliseconds/1000) % 60, 3)
        minutes = (milliseconds/(1000*60)) % 60
        minutes = int(minutes)
        hours = int((milliseconds/(1000*60*60)) % 24)
        time = ""
        if hours > 0:
            time = "{} hour".format(hours)
        if hours > 1:
            time +="s"
        if minutes > 0:
            time += " {} minute".format(minutes)
        if minutes > 1:
            time += "s"
        if seconds > 0:
            time  += " {} second".format(seconds)
        if seconds > 1:
            time += "s"
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
        return self.millisecondsToTimeStamp(millis)


if __name__ == "__main__":
    utils = Utils()
    result = utils.millisecondsToTimeStamp(14643000)
    print(result)
    result = utils.millisecondsToTimeStamp(268000)
    print(result)