#!/usr/bin/env python3




class Utils():
    def __init__(self):
        pass

    def secondsToTimeStamp(self, seconds):
        minutes = int((seconds / 60) % 60)
        hours = int((seconds / (60*60)) % 3600)
        sec = int(seconds - (minutes * 60) - (hours * 60 *60))
        time = ""
        if hours >= 1:
            time = "{} hours ".format(hours)
        if minutes >= 1:
            time += "{} minutes ".format(minutes)
        if sec >= 1:
            time  += "{} seconds".format(sec)
        return time


    def timeStamp(self,duration,current):
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
    result = utils.secondsToTimeStamp(14643)
    print(result)
    result = utils.secondsToTimeStamp(268)
    print(result)