import math
import random

import settings
from utils import randint_except


class Person(object):
    def __init__(self, id_, x=0, y=0, nose=(1, 0)):
        self.id = id_
        self.x = x
        self.y = y
        self.nose = nose
        self.target = None

    def __str__(self):
        return '{}: ({}, {})'.format(self.id, self.x, self.y)


class Party(object):
    def __init__(self):
        self.persons = []  # type: List[Person]

    def setup(self):
        self.persons = []  # .clear(), Py >= 3.3
        n = settings.get().number_of_people
        for i in range(n):
            angle = random.random() * math.pi * 2
            nose = math.cos(angle), math.sin(angle)
            x, y = random.random(), random.random()
            person = Person(i, x, y, nose)
            person.target = randint_except(0, n - 1, i)
            self.persons.append(person)

    def update(self):
        def turn_toward(nose, target):
            vx, vy = nose

            # 1. current target vector
            ttx, tty = target.x - p.x, target.y - p.y

            # 2. current target versor
            d = math.hypot(ttx, tty)
            if d < 1e-12:  # too short distance - don't turn nose
                return nose
            tx, ty = ttx / d, tty / d

            # 3. vector sum
            nx, ny = vx + tx, vy + ty
            d = math.hypot(nx, ny)
            if d < 1e-12:  # probably going opposite distance, turn 90*
                return -vy, vx

            # 4. new speed versor
            return nx / d, ny / d

        def jitter():
            return random.gauss(0, 0.7) * settings.get().person_speed

        v = settings.get().person_speed
        d_min = settings.get().target_distance_min
        updated = False

        for p in self.persons:
            target_p = self.persons[p.target]

            vx, vy = p.nose = turn_toward(p.nose, target_p)
            d = math.hypot(target_p.x - p.x, target_p.y - p.y)

            if d_min / 2 < d < d_min:
                # good distance
                continue

            if d < d_min / 2:
                # too close, switch to reverse gear
                move_x, move_y = -v * vx, -v * vy
            else:
                # standard walk
                move_x, move_y = v * vx, v * vy

            new_pos_x, new_pos_y = p.x + move_x, p.y + move_y

            # rudimentary collision check
            min_distance_to_other = min(
                math.hypot(new_pos_x - op.x, new_pos_y - op.y)
                for op in self.persons
                if op.id not in (p.id, p.target)
            )

            if min_distance_to_other < settings.get().min_distance_to_other:
                if settings.get().jitter:
                    p.x, p.y = p.x - move_x / 2 + jitter(), p.y - move_y / 2 + jitter()
                    updated = True
                continue

            updated = True
            p.x, p.y = new_pos_x, new_pos_y

        return updated
