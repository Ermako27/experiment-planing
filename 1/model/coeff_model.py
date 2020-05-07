import numpy

from model.lab_model import LabModel


class CoefficientModel:
    def __init__(self):
        self._count_factors = 3
        self.count_experiments = pow(2, self._count_factors)

        self.x_values_matrix = self.get_x_matrix(self.count_experiments, self._count_factors)
        self.x12_vector = self.get_x_vector(self.x_values_matrix, 0, 1)
        self.x13_vector = self.get_x_vector(self.x_values_matrix, 0, 2)
        self.x23_vector = self.get_x_vector(self.x_values_matrix, 1, 2)

        self.y_practice_vector = numpy.zeros(self.count_experiments)

        self._limit_matrix = numpy.zeros((self._count_factors, 2))

        self.line_coefficients_list = numpy.zeros(4)
        self.no_line_coefficients_list = numpy.zeros(7)
        self.y_predict_vector = numpy.zeros(self.count_experiments)

    def reset(self):
        self.y_practice_vector = numpy.zeros(self.count_experiments)
        self._limit_matrix = numpy.zeros((self._count_factors, 2))
        self.line_coefficients_list = numpy.zeros(4)
        self.no_line_coefficients_list = numpy.zeros(7)
        self.y_predict_vector = numpy.zeros(self.count_experiments)

    def fill_limit_matrix(self, lambda_tuple: tuple, mu_tuple: tuple, sigma_tuple: tuple):
        self._limit_matrix[0][0], self._limit_matrix[0][1] = lambda_tuple
        self._limit_matrix[1][0], self._limit_matrix[1][1] = mu_tuple
        self._limit_matrix[2][0], self._limit_matrix[2][1] = sigma_tuple

    def fill_y_practice_vector(self, model: LabModel):
        # print('self._limit_matrix', self._limit_matrix, self.count_experiments)
        for i in range(self.count_experiments):
            index_lambda = int(self.x_values_matrix[i][0] > 0)
            index_mu = int(self.x_values_matrix[i][1] > 0)
            index_sigma = int(self.x_values_matrix[i][2] > 0)

            print('Произвольная точка')
            print('x1 ', 1 / self._limit_matrix[0][index_lambda])
            print('x2 ', 1 / self._limit_matrix[1][index_mu])
            print('x3 ', self._limit_matrix[2][index_sigma])
            # print('here 2')
            for data in model.simulation(self._limit_matrix[0][index_lambda], self._limit_matrix[1][index_mu],
                                         self._limit_matrix[2][index_sigma]):
                self.y_practice_vector[i] = data[2]
            
            # print('self.y_practice_vector', self.y_practice_vector)
            print('y  ', self.y_practice_vector[i])

    def eval_coefficients(self):
        x_matrix = numpy.concatenate((numpy.ones((1, self.count_experiments)), self.x_values_matrix.T,
                                      self.x12_vector.reshape((1, self.count_experiments)),
                                      self.x13_vector.reshape((1, self.count_experiments)),
                                      self.x23_vector.reshape((1, self.count_experiments))),
                                     axis=0)

        for i in range(len(x_matrix)):
            self.no_line_coefficients_list[i] = (x_matrix[i] * self.y_practice_vector).sum() / self.count_experiments

            if i < len(self.line_coefficients_list):
                self.line_coefficients_list[i] = self.no_line_coefficients_list[i].copy()

        self.y_predict_vector = numpy.dot(self.no_line_coefficients_list, x_matrix)
        print('y\' ', self.y_predict_vector[7])
        print('y-y\' ', self.y_practice_vector[7] - self.y_predict_vector[7])
        index_lambda = int(self.x_values_matrix[7][0] > 0)
        index_mu = int(self.x_values_matrix[7][1] > 0)
        index_sigma = int(self.x_values_matrix[7][2] > 0)
        yravnenie = self.line_coefficients_list[0] + self.line_coefficients_list[1]*self._limit_matrix[0][index_lambda] \
        + self.line_coefficients_list[2]*self._limit_matrix[1][index_mu] + self.line_coefficients_list[3]*self._limit_matrix[2][index_sigma]
        yravnenie2 = self.no_line_coefficients_list[0] + self.no_line_coefficients_list[1] * self._limit_matrix[0][index_lambda] \
        + self.no_line_coefficients_list[2] * self._limit_matrix[1][index_mu] + self.no_line_coefficients_list[3] * self._limit_matrix[2][index_sigma] \
        + self.no_line_coefficients_list[4] * self._limit_matrix[0][index_lambda] * self._limit_matrix[1][index_mu] + \
        + self.no_line_coefficients_list[5] * self._limit_matrix[0][index_lambda] * self._limit_matrix[2][index_sigma] + \
        + self.no_line_coefficients_list[6] * self._limit_matrix[1][index_mu] * self._limit_matrix[2][index_sigma]

        print ('y* ', yravnenie)
        print ('y^ ', yravnenie2)

    def function(self, x_vector: numpy.ndarray) -> float:
        return float(numpy.dot(self.no_line_coefficients_list, x_vector.reshape(x_vector.shape[::-1])))

    def line_function(self, x_vector: numpy.ndarray) -> float:
        return float(numpy.dot(self.line_coefficients_list, x_vector.reshape(x_vector.shape[::-1])))  # + 0.63290413

    def get_function(self) -> str:
        str_list = list(map(lambda x: f'+ {round(x, 10)}' if x >= 0 else f'- {abs(round(x, 10))}',
                            self.no_line_coefficients_list))

        str_x = [f'x_{i}' for i in range(4)] + ['x_12', 'x_13', 'x_23']

        import functools
        function = functools.reduce(lambda x, y: f'{x} {y}', [f'{x} * {y}' for x, y in zip(str_list, str_x)])
        if function[0] == '+':
            function = function[2:]
        return function

    @property
    def get_diff_y(self):
        return self.y_practice_vector - self.y_predict_vector

    @property
    def get_diff_y_pow_2(self):
        return pow(self.get_diff_y, 2)

    @staticmethod
    def get_x_vector(matrix: numpy.ndarray, i: int, j: int) -> numpy.ndarray:
        vector = numpy.zeros(len(matrix), dtype=int)
        for k in range(len(matrix)):
            vector[k] = matrix[k][i] * matrix[k][j]
        return vector

    @staticmethod
    def get_x_matrix(row_count: int, col_count: int) -> numpy.ndarray:
        matrix = numpy.zeros((row_count, col_count), dtype=int).T
        for i in range(len(matrix)):
            val = -1
            count = 0
            for j in range(len(matrix[i])):
                matrix[i][j] = val
                count += 1
                if count % pow(2, i) == 0:
                    count = 0
                    val *= -1
        matrix = matrix.T

        return matrix
