#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import atexit
import random
import shutil
import time
import string

CSI = '\x1b['
MAP = {
    'reset' : 0, 'bold' : 1,
    'clear' : 39, 'bg_clear'  : 49,

    'black'  : 30, 'lt_black'  : 90,
    'red'    : 31, 'lt_red'    : 91,
    'green'  : 32, 'lt_green'  : 92,
    'yellow' : 33, 'lt_yellow' : 93,
    'blue'   : 34, 'lt_blue'   : 94,
    'purple' : 35, 'lt_purple' : 95,
    'cyan'   : 36, 'lt_cyan'   : 96,
    'white'  : 37, 'lt_white'  : 97,

    'bg_black'  : 40, 'bg_lt_black'  : 100,
    'bg_red'    : 41, 'bg_lt_red'    : 101,
    'bg_green'  : 42, 'bg_lt_green'  : 102,
    'bg_yellow' : 43, 'bg_lt_yellow' : 103,
    'bg_blue'   : 44, 'bg_lt_blue'   : 104,
    'bg_purple' : 45, 'bg_lt_purple' : 105,
    'bg_cyan'   : 46, 'bg_lt_cyan'   : 106,
    'bg_white'  : 47, 'bg_lt_white'  : 107,
    }


class Write(object):
    def __init__(self):
        self._enabled = True
        if not sys.stdout.isatty():
            self._enabled = False

    def __call__(self, fmt='', *args):
        sys.stdout.write(fmt % args)
        return self

    def __getitem__(self, name):
        if isinstance(name, str):
            name = (name,)
        for n in name:
            sys.stdout.write(CSI+'%dm' % MAP.get(n))
        return self

    def __getattr__(self, name):
        sys.stdout.write(CSI+'%dm' % MAP.get(name))
        return self

write = Write()


mono  = ['white','black','lt_black','lt_white']
reds  = ['red','lt_red','purple','lt_purple']
blues = ['blue','lt_blue','cyan','lt_cyan']

spectrum = ['black', 'lt_black', 'red', 'lt_red', 'green', 'lt_green', 'yellow', 'lt_yellow', 'blue', 'lt_blue', 'purple', 'lt_purple', 'cyan', 'lt_cyan', 'white', 'lt_white']


#blocks = ['▀','▁','▂','▃','▄','▅','▆','▇','█','▉','▊','▋','▌','▍','▎','▏','▐','░','▒','▓','▔','▕','▖','▗','▘','▙','▚','▛','▜','▝','▞','▟',]
blocks = '▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟'
other = '■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄◅◆◇◈◉◊○◌◍◎●◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯◰◱◲◳◴◵◶◷◸◹◺◻◼◽◾◿'

def SattoloShuffle(items):
    i = len(items)
    while i > 1:
        i = i - 1
        j = random.randrange(i)  # 0 <= j <= i-1
        items[j], items[i] = items[i], items[j]
    return items


class Mover(object):
    UP   = CSI+'1A'
    DOWN = CSI+'1B'

    def __init__(self, chars, colors):
        self.chars  = chars
        self.colors = colors

    def run(self):
        raise NotImplementedError


class Blotch(Mover):
    class Mover(object):
        def __init__(self, mover):
            self.mover = mover
            self.n()
            self.x = random.randrange(console.cols) + 1
            self.y = random.randrange(console.rows) + 1
            self.count = 0

        def n(self):
            self.color   = random.choice(self.mover.colors)
            #self.bgcolor = 'bg_' + random.choice(self.mover.colors + ['clear'])
            self.g = random.choice(self.mover.chars)
            self.max = random.randrange(100,300)

        def move(self):
            self.x += random.randint(-1,1)
            self.y += random.randint(-1,1)
            self.x = max(0,self.x)
            self.y = max(0,self.y)
            self.x = min(console.cols,self.x)
            self.y = min(console.rows,self.y)
            sys.stdout.write('\033[%d;%dH' % (self.y,self.x))
            #write[self.color][self.bgcolor]('%s', self.g)
            write[self.color]('%s', self.g)

            try:
                self.mover.board.remove((self.y,self.x))
            except ValueError:
                pass

            self.count += 1
            if self.count > self.max:
                self.n()
                self.count = 0

    def run(self):
        self.board = []
        for i in range(console.rows):
            for j in range(console.cols):
                self.board.append((i+1,j+1))

        movers = [Blotch.Mover(self) for _ in range(20)]
        while self.board:
            for m in movers:
                m.move()
            sys.stdout.flush()
            time.sleep(1 / 60.0)
            #time.sleep(0.001)



class HorizontalLines(Mover):
    def __init__(self, *args, **kwds):
        super(HorizontalLines, self).__init__(*args, **kwds)
        self.count = 0
        self.directions = [CSI+'1A', CSI+'1B', '']

    def run(self):
        count = random.randrange(50,300)
        for _ in range(count):
            self.drawone()

    def drawone(self):
        g = random.choice(self.chars)
        write[random.choice(self.colors)]
        write['bg_' + random.choice(self.colors + ['clear'])]
        #getattr(write, random.choice(c))
        #getattr(write, 'bg_'+random.choice(c))
        console.abs(random.randrange(1,console.rows), 1)

        for _ in range(console.cols):
            d = random.choice(self.directions)
            sys.stdout.write(d)
            #sys.stdout.buffer.write(chr(random.randrange(33,127)).encode('utf-8'))
            sys.stdout.write(g)
            sys.stdout.flush()
            time.sleep(0.001)


class Clear(object):
    def run(self):
        board = []
        for i in range(console.rows):
            for j in range(console.cols):
                board.append((i+1,j+1))

        p = random.choice(palettes)

        write[random.choice(p)]['bg_' + random.choice(p)]

        x = random.choice(random.choice(sequences))

        SattoloShuffle(board)

        while board:
            i = board.pop()
            #i = random.choice(board)
            #board.remove(i)
            console.abs(*i)
            #print(len(board))
            sys.stdout.write(x)
            sys.stdout.flush()
            time.sleep(0.001)

class Console(object):
    def __init__(self):
        if not sys.stdout.isatty():
            raise IOError('Not a TTY')

        sys.stdout.write(CSI+'?25l')
        sys.stdout.write(CSI+'2J')
        sys.stdout.write(CSI+'1;1H')

        dim = shutil.get_terminal_size()
        self.cols = dim.columns
        self.rows = dim.lines
        atexit.register(self.exit)

    def abs(self, y, x):
        sys.stdout.write('\033[%d;%dH' % (y,x))

    def exit(self):
        sys.stdout.write(CSI+'?25h')
        write.reset
        self.abs(self.rows,1)


try:
    console = Console()
except IOError:
    pass

sequences = [
    blocks,
    #string.punctuation,
    #string.ascii_letters,
    #string.digits,
    #other,
    '░▒▓█'
    #'▚'
    ]

palettes = [
    #mono,
    #reds,
    #blues,
    mono + reds,
    mono + blues,
    reds + blues,
    #spectrum,
]


try:
    while True:
        s = random.choice(sequences)
        p = random.choice(palettes)
        hz = Blotch(s,p)
        hz.run()

        Clear().run()
        s = random.choice(sequences)
        p = random.choice(palettes)
        hz = HorizontalLines(s,p)
        hz.run()

        Clear().run()

except KeyboardInterrupt:
    pass

#write.red('hello\n')
#write(''.join(blocks))
#write('\n')
#time.sleep(2)
