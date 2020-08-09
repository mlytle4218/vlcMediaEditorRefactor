#!/usr/env python3
import pytest
from main import fileActions


fa = fileActions.FileActions('rusty-original.mp3')

def test_one():

    assert fa.stateFile == '/home/marc/Desktop/chime/vlcMediaEditor/rusty-original.state'