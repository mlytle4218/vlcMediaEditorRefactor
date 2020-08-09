#!/usr/bin/env python3
import logging

from main import mark


class MarkControls():
    def __init__(self):
        # self.state = state
        self.currentMark = None

    def startMark(self, currentPos):
        if not self.currentMark:
            self.currentMark = mark.Mark(position=currentPos)
            self.updateScreen('Edit point started.')
        else:
            self.currentMark.start = currentPos
            self.updateScreen('Edit point updated')

    def endMark(self, currentPos):
        if not self.currentMark:
            self.updateScreen('No Edit point to End')
        else:
            self.currentMark = currentPos
            self.updateScreen('Edit point ended')
            self.state.marks.append(self.currentMark)
            self.currentMark = None

    # def updateScreen(self, message):
    #     self.state.print_to_screen(message)

            