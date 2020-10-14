#!/usr/bin/env python3

import wave, sys

def play_audio(filename):
    print(filename)
    f = wave.open(filename, mode='rb')
    print(f.getchannels())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass a file name\n")
        exit(0)
    #print(sys.argv)
    play_audio(sys.argv[1])
     