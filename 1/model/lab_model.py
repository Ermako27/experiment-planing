from model.generator import RequestGenerator, ExponentialGenerator, NormalGenerator
from utility.lab_observer import LabObserver
from model.processor import Processor


class LabModel:
    def __init__(self):
        self._observers = set()

        self.exp_lambda = None
        self.a = None
        self.b = None

        self.count_request = None

        self._intensity_generator = None
        self._intensity_processor = None

        self._generator = None
        self._processor = None

    def simulation(self, exp_lambda: float = None, b: float = None, a: float = None,
                   count_request: int = 100):
        if exp_lambda is None:
            exp_lambda = self.exp_lambda
        if a is None:
            a = self.a
        if b is None:
            b = self.b
        if count_request is None:
            count_request = self.count_request

        # print('norm SIGMA', a)
        #v8
        # self._generator = RequestGenerator(NormalGenerator(a, b))
        # self._processor = Processor(ExponentialGenerator(exp_lambda))

        ##################################
        self._generator = RequestGenerator(ExponentialGenerator(exp_lambda))
        self._processor = Processor(NormalGenerator(a, b))

        self._generator.add_receiver(self._processor)

        times = [self._generator, self._processor]
        current_time = 0

        while self._processor.requests_processed < count_request:
            current_time += times[0].next_eval_time
            for i in range(len(times) - 1, -1, -1):
                times[i].time_pass(times[0].next_eval_time)

            times[0].process()
            times.sort(key=lambda x: x.next_eval_time)

            gen_int = self._generator.intensity
            pro_int = self._processor.intensity
            if pro_int != 0:
                load = gen_int / pro_int
            else:
                load = 0

            yield (gen_int, pro_int, load,
                   self._processor.requests_processed, current_time)

    def add_observer(self, observer: LabObserver):
        self._observers.add(observer)

    def remove_observer(self, observer: LabObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.model_is_changed()
