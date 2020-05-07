from math import inf

from model.generator import BaseGenerator


class BaseRequestReceiver:
    def __init__(self):
        self._flag_busy = False
        self._requests_processed = 0
        self._requests_passed = 0
        self._current_queue_size = 0
        self._max_queue_size = 0
        self._next_eval_time = inf

    def receive_request(self):
        raise NotImplementedError()

    def process(self):
        raise NotImplementedError()

    @property
    def flag_busy(self) -> bool:
        return self._flag_busy

    @property
    def requests_processed(self) -> int:
        return self._requests_processed

    @property
    def requests_passed(self) -> int:
        return self._requests_passed

    @property
    def next_eval_time(self) -> float:
        return self._next_eval_time

    @next_eval_time.setter
    def next_eval_time(self, value: float) -> None:
        self._next_eval_time = value


class Processor(BaseRequestReceiver, BaseGenerator):
    def __init__(self, generator: BaseGenerator, *args, **kwargs):
        self._generator = generator
        self._count = 0
        self._sum_time = 0
        super().__init__(*args, **kwargs)

    def receive_request(self):
        if not self._flag_busy:
            self._flag_busy = True
            self._next_eval_time = self.next()
        else:
            self._current_queue_size += 1
            if self._current_queue_size > self._max_queue_size:
                self._max_queue_size = self._current_queue_size

    def process(self):
        self._requests_processed += 1
        self._flag_busy = False
        self._next_eval_time = inf

        if self._current_queue_size > 0:
            self._current_queue_size -= 1
            self._flag_busy = True
            self._next_eval_time = self.next()

    def time_pass(self, delta_time: int):
        self._next_eval_time -= delta_time

    def next(self):
        t = self._generator.next()
        self._count += 1
        self._sum_time += t
        return t

    @property
    def max_queue_size(self) -> int:
        return self._max_queue_size

    @property
    def intensity(self) -> float:
        if self._sum_time != 0:
            return 1 / (self._sum_time / self._count)
        else:
            return 0
