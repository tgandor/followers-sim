from __future__ import print_function, division, absolute_import

import settings
from model import Party
from utils import color_for_id

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter


class PersonPainter(object):
    def __init__(self, canvas, person):
        self.canvas = canvas
        self.person = person
        self.oval = None
        self.nose = None
        self.update()

    def update(self):
        s = settings.get().dot_size
        w = h = settings.get().canvas_size - s
        x, y = w * self.person.x, h * self.person.y

        if self.oval is None:
            self.oval = self.canvas.create_oval((x, y, x + s, y + s), fill=color_for_id(self.person.id))
        else:
            self.canvas.coords(self.oval, x, y, x + s, y + s)

        cx, cy = x + s / 2, y + s / 2
        dx, dy = s * self.person.nose[0], s * self.person.nose[1]

        if self.nose is None:
            self.nose = self.canvas.create_line((cx, cy, cx + dx, cy + dy))
        else:
            self.canvas.coords(self.nose, cx, cy, cx + dx, cy + dy)


class MainWindow(object):
    def __init__(self, parent):
        # GUI init
        self.parent = parent
        self.parent.title("9.3 Crowded Room")
        self.frame = tkinter.Frame(self.parent)
        self.frame.pack(fill=tkinter.BOTH, expand=1)
        tkinter.Label(self.frame, text='Crowded room simulation').pack()
        size = settings.get().canvas_size
        self.canvas = tkinter.Canvas(self.frame, width=size, height=size)
        self.canvas.pack()
        tkinter.Button(self.frame, text='Prepare', command=self.setup_simulation).pack(fill='x')
        tkinter.Button(self.frame, text='Start', command=self.start_simulation).pack(fill='x')
        tkinter.Button(self.frame, text='Stop', command=self.stop_simulation).pack(fill='x')
        self.parent.resizable(width=tkinter.FALSE, height=tkinter.FALSE)

        # create model
        self.party = Party()

        # intermediate logic
        self.person_painters = []  # type: List[PersonPainter]
        self.prepared = False
        self.running = False

    def _step_simulation(self):
        if not self.running:
            return

        # only keep running if modifications present
        self.running = self.party.update()

        if self.running:
            for p in self.person_painters:
                p.update()
            self.frame.after(50, self._step_simulation)

    def stop_simulation(self):
        self.running = False

    def start_simulation(self):
        if self.running:
            print('Already running')
            return

        if not self.prepared:
            print('Simulation not ready')
            return

        self.running = True
        self._step_simulation()

    def setup_simulation(self):
        if self.running:
            print('Not while running')
            return

        self.canvas.delete('all')
        self.party.setup()
        self.person_painters = []
        for p in self.party.persons:
            self.person_painters.append(PersonPainter(self.canvas, p))
        self.prepared = True


if __name__ == '__main__':
    root = tkinter.Tk()
    main_window = MainWindow(root)
    root.mainloop()
