import math
from abc import ABC

class Interest(ABC):
    def __repr__(self):
        return f'mensual: {self.pm:.3f}, anual: {self.pa:.2f}'

    def __init__(self):
        self.pm = 0
        self.pa = 0

    def mensual(self):
        return self.pm

    def anual(self):
        return self.pa


class IntYearly(Interest):
    def __init__(self, p: float):
        assert p < 1
        self.pm = (1+p) ** (1/12) - 1
        self.pa = p

class IntMonthly(Interest):
    def __init__(self, p: float):
        assert p < 1
        self.pm = p
        self.pa = (1+p) ** 12 - 1


class Decu:
    def __repr__(self):
        return f'Decu: s: {self.s:.0f}, j: {self.j} p: {self.p}'

    def __init__(self, s: float, p: Interest, j: float):
        self.s = s
        self.p = p
        self.j = j

    def time_span(self):
        s = self.s
        n = 0
        while True:
            t = s*(1+self.p.pm) - self.j
            if s <= t:
                return math.inf, None
            if t < 0:
                break
            s = t
            n += 1
        return n, s

    def evol(self, n):
        s = self.s
        hist = [s]
        for _ in range(n):
            s = s*(1+self.p.pm) - self.j
            hist.append(s)
        return hist,s

class Acu:
    def __repr__(self):
        return 'Acu: ' + \
            f'init: {self.inicial:.0f}, years: {self.years}, ah: {self.a} p: {self.p}'

    def __init__(self, years:float, p:Interest, a:float, inicial:float=0):
        self.years = years
        self.p = p
        self.a = a
        self.inicial = inicial

    def evol(self):
        s = self.inicial 
        for _ in range(12 * self.years):
            s = s*(1+self.p.pm) + self.a
        return s

class AcDec:
    def __init__(
            self, years: float, int_anual: float, j: float, a: float, init:float
        ):
        self.y = years
        self.p = IntYearly(int_anual)
        self.j = j
        self.a = a
        self.init = init
        self.acu = Acu(self.y, self.p, self.a, self.init)
        self.decu = Decu(self.acu.evol(), self.p, self.j)
        self.span, _  = self.decu.time_span()


    def __repr__(self):
        return f'y: {self.y}, p: {self.p}, j: {self.j}, a: {self.a}\n' +\
               f'{self.acu}\n{self.decu}\n' +\
               f'span: {self.span/12:.1f} años'
               

x = AcDec(10, .02, 750, 1500, 0)

