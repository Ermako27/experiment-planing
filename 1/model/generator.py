from abc import ABC

from numpy import random


class BaseGenerator:
    def next(self) -> float:
        raise NotImplementedError()


class ExponentialGenerator(BaseGenerator):
    def __init__(self, lmd: float):
        assert lmd >= 0

        self._lambda = lmd

    def next(self) -> float:
        return random.exponential(self._lambda)

class UniformGenerator(BaseGenerator):
    def __init__(self, a, b):
        if not 0 <= a <= b:
            raise ValueError('Параметры должны удовлетворять условию 0 <= a <= b')
        self._a = a
        self._b = b

    def next(self):
        return random.uniform(self._a, self._b)

class NormalGenerator(BaseGenerator):
    def __init__(self, sigma: float, mu: float):
        assert sigma >= 0

        self._sigma = sigma
        self._mu = mu

    def next(self) -> float:
        value = random.normal(self._mu, self._sigma)
        if value < 0:
            value = 0
        return value


class BaseRequestGenerator(BaseGenerator, ABC):
    def __init__(self, *args, **kwargs):
        self._receivers = set()
        super().__init__(*args, **kwargs)

    def add_receiver(self, receiver):
        self._receivers.add(receiver)

    def remove_receiver(self, receiver):
        if receiver in self._receivers:
            self._receivers.remove(receiver)

    def emit_request(self):
        for receiver in self._receivers:
            receiver.receive_request()


class RequestGenerator(BaseRequestGenerator):
    def __init__(self, generator: BaseGenerator, *args, **kwargs):
        self._generator = generator
        self._count = 0
        self._sum_time = 0
        self._next_eval_time = self.next()
        super().__init__(*args, **kwargs)

    def process(self):
        self.emit_request()
        self._next_eval_time = self.next()

    def next(self):
        t = self._generator.next()
        self._count += 1
        self._sum_time += t
        return t

    @property
    def next_eval_time(self) -> float:
        return self._next_eval_time

    @next_eval_time.setter
    def next_eval_time(self, value: float) -> None:
        assert value >= 0
        self._next_eval_time = value

    def time_pass(self, value: float):
        self._next_eval_time -= value

    @property
    def intensity(self) -> float:
        return 1 / (self._sum_time / self._count)
