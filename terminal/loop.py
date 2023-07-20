#!/usr/bin/env python3

import sys
import os
import atexit
import random
import shutil
import string
import time

from PIL import Image

out = os.fdopen(sys.stdout.fileno(), 'wb', 0)

CSI = b'\x1b['

def SattoloShuffle(items):
    i = len(items)
    while i > 1:
        i = i - 1
        j = random.randrange(i)
        items[j], items[i] = items[i], items[j]
    return items


markings = [
    string.ascii_uppercase,
    string.ascii_lowercase,
    string.punctuation,
    '▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟',
    '▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄◅',
    '●',
    ]

SattoloShuffle(markings)

class Console(object):
    def __init__(self):
        if not sys.stdout.isatty():
            raise IOError('Not a TTY')

        out.write(CSI+b'?25l')
        out.write(CSI+b'2J')
        out.write(CSI+b'1;1H')

        atexit.register(self.exit)

        dim = shutil.get_terminal_size()
        self.cols = dim.columns
        self.rows = dim.lines


    def exit(self):
        out.write(CSI+b'?25h')
        out.write(CSI+b'0m')
        out.write(b'\033[1;1H')

    def run(self, path):

        im = Image.open(path)
        im = im.resize((console.cols, console.rows))

        num = range(8)

        col = [random.randrange(self.cols) for i in num]
        row = [random.randrange(self.rows) for i in num]

        #col = random.randrange(self.cols)
        #row = random.randrange(self.rows)

        delta = 16

        maxcount = self.rows * self.cols * 1
        count = 0
        try:
            #marking = random.choice(markings)
            marking = markings.pop(0)
            markings.append(marking)

            while count < maxcount:
                for i in num:
                    col[i] = max(1, min(self.cols, col[i] + random.randint(-2,2)))
                    row[i] = max(1, min(self.rows, row[i] + random.randint(-2,2)))

                    (r,g,b) = im.getpixel((col[i]-1,row[i]-1))
                    r = max(0, min(255, r + random.randint(-delta,delta)))
                    g = max(0, min(255, g + random.randint(-delta,delta)))
                    b = max(0, min(255, b + random.randint(-delta,delta)))

                    c = random.choice(marking).encode('utf-8')
                    #'■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄◅◆◇◈◉◊○◌◍◎●◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯◰◱◲◳◴◵◶◷◸◹◺◻◼◽◾◿'
                    #c = '●'

                    out.write(b'\033[%d;%dH' % (row[i],col[i]))
                    out.write(b'\033[38;2;%d;%d;%dm%s' % (r,g,b,c))
                count += 1

                #sys.stdout.flush()
                time.sleep(0.001)
        except KeyboardInterrupt:
            pass

    def clear(self):
        board = []
        for i in range(self.rows):
            for j in range(self.cols):
                board.append((i+1,j+1))

        SattoloShuffle(board)
        #x = random.choice(random.choice(sequences))
        while board:
            i = board.pop()
            #i = random.choice(board)
            #board.remove(i)
            out.write(b'\033[%d;%dH' % i)
            out.write(b' ')
            #sys.stdout.flush()
            #time.sleep(0.005)



try:
    console = Console()
except IOError:
    pass

inputs = sys.argv[1:]
inputs = SattoloShuffle(inputs)

for p in inputs:
    console.run(p)
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

    try:
        console.clear()
    except KeyboardInterrupt:
        pass
