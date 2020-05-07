from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit

from model.coeff_model import CoefficientModel
from model.lab_model import LabModel
from view.lab_view import LabView


class LabController:
    def __init__(self, in_model: LabModel):
        self.c_model = in_model
        self.c_coefficient_model = CoefficientModel()
        self.c_view = LabView(self, self.c_model)

        self.c_view.show()

    def srcReqLambdaIntChange(self, value: float):
        if value != 0.0:
            value = 1 / value
        self.c_view.ui.dblSpinBoxSrcReqLambdaTime.setValue(value)

    def srcReqLambdaTimeChange(self, value: float):
        if value != 0.0:
            value = 1 / value
        self.c_view.ui.dblSpinBoxSrcReqLambdaInt.setValue(value)

    def srcReqMuIntChange(self, value: float):
        if value != 0.0:
            value = 1 / value
        self.c_view.ui.dblSpinBoxServiceReqMuTime.setValue(value)

    def srcReqMuTimeChange(self, value: float):
        if value != 0.0:
            value = 1 / value
        self.c_view.ui.dblSpinBoxServiceReqMuInt.setValue(value)

    def _set_theory_results(self):
        self.c_view.ui.dblSpinBoxResultIntensitySrcTheory.setValue(
            self.c_view.ui.dblSpinBoxSrcReqLambdaInt.value())
        self.c_view.ui.dblSpinBoxResultsIntensityServiceTheory.setValue(
            self.c_view.ui.dblSpinBoxServiceReqMuInt.value())
        self.c_view.ui.dblSpinBoxResultsLoadTheory.setValue(
            self.c_view.ui.dblSpinBoxSrcReqLambdaInt.value() / self.c_view.ui.dblSpinBoxServiceReqMuInt.value())

    def simulate(self):
        self._set_theory_results()

        self.c_model.exp_lambda = self.c_view.ui.dblSpinBoxSrcReqLambdaTime.value()
        self.c_model.a = self.c_view.ui.dblSpinBoxServiceReqSigma.value()
        self.c_model.b = self.c_view.ui.dblSpinBoxServiceReqMuTime.value()
        self.c_model.count_request = self.c_view.ui.spinBoxSettingsCount.value()

        self.c_model.notify_observers()

    def eval_coefficients(self):
        # print('eval_coefficients !!!!!!!!!!!!!!!!!!!!')
        self.c_coefficient_model.reset()
        lambda_tuple = (1 / self.c_view.ui.dblSpinBoxLevelsVarLambdaFrom.value(),
                        1 / self.c_view.ui.dblSpinBoxLevelsVarLambdaTo.value())
        mu_tuple = (1 / self.c_view.ui.dblSpinBoxLevelsVarMuFrom.value(),
                    1 / self.c_view.ui.dblSpinBoxLevelsVarMuTo.value())
        sigma_tuple = (self.c_view.ui.dblSpinBoxLevelsVarSigmaFrom.value(),
                       self.c_view.ui.dblSpinBoxLevelsVarSigmaTo.value())
        self.c_coefficient_model.fill_limit_matrix(lambda_tuple, mu_tuple, sigma_tuple)
        self.c_coefficient_model.fill_y_practice_vector(self.c_model)
        self.c_coefficient_model.eval_coefficients()

        self.update_tables()

        self.c_view.statusBar().showMessage('Уравнение: ' + self.c_coefficient_model.get_function())
        print('Уравнение: ' + self.c_coefficient_model.get_function())

    def update_tables(self):
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffLineB0, self.c_coefficient_model.line_coefficients_list[0])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffLineB1, self.c_coefficient_model.line_coefficients_list[1])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffLineB2, self.c_coefficient_model.line_coefficients_list[2])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffLineB3, self.c_coefficient_model.line_coefficients_list[3])

        self.set_line_edit_value(self.c_view.ui.lineEditCoeffNoLineB0,
                                 self.c_coefficient_model.no_line_coefficients_list[0])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffNoLineB1,
                                 self.c_coefficient_model.no_line_coefficients_list[1])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffNoLineB2,
                                 self.c_coefficient_model.no_line_coefficients_list[2])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffNoLineB3,
                                 self.c_coefficient_model.no_line_coefficients_list[3])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffNoLineB12,
                                 self.c_coefficient_model.no_line_coefficients_list[4])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffNoLineB13,
                                 self.c_coefficient_model.no_line_coefficients_list[5])
        self.set_line_edit_value(self.c_view.ui.lineEditCoeffNoLineB23,
                                 self.c_coefficient_model.no_line_coefficients_list[6])

        for i in range(self.c_coefficient_model.count_experiments):
            for j in range(len(self.c_coefficient_model.x_values_matrix[i])):
                cell_info_x_matrix = QTableWidgetItem(str(self.c_coefficient_model.x_values_matrix[i][j]))
                self.c_view.ui.tableWidgetLineModel.setItem(i, j, cell_info_x_matrix)
                cell_info_x_matrix = cell_info_x_matrix.clone()
                self.c_view.ui.tableWidgetNoLineModel.setItem(i, j, cell_info_x_matrix)

            cell_info_x12 = QTableWidgetItem(str(self.c_coefficient_model.x12_vector[i]))
            self.c_view.ui.tableWidgetNoLineModel.setItem(i, 3, cell_info_x12)
            cell_info_x13 = QTableWidgetItem(str(self.c_coefficient_model.x13_vector[i]))
            self.c_view.ui.tableWidgetNoLineModel.setItem(i, 4, cell_info_x13)
            cell_info_x23 = QTableWidgetItem(str(self.c_coefficient_model.x23_vector[i]))
            self.c_view.ui.tableWidgetNoLineModel.setItem(i, 5, cell_info_x23)

            cell_info_y_practice = QTableWidgetItem(str(round(self.c_coefficient_model.y_practice_vector[i], 3)))
            self.c_view.ui.tableWidgetLineModel.setItem(i, 3, cell_info_y_practice)
            cell_info_y_practice = cell_info_y_practice.clone()
            self.c_view.ui.tableWidgetNoLineModel.setItem(i, 6, cell_info_y_practice)

            cell_info_y_predict = QTableWidgetItem(str(round(self.c_coefficient_model.y_predict_vector[i], 3)))
            self.c_view.ui.tableWidgetLineModel.setItem(i, 4, cell_info_y_predict)
            cell_info_y_predict = cell_info_y_predict.clone()
            self.c_view.ui.tableWidgetNoLineModel.setItem(i, 7, cell_info_y_predict)

            diff_y = self.c_coefficient_model.get_diff_y
            cell_info_diff_y = QTableWidgetItem(str(round(diff_y[i], 3)))
            self.c_view.ui.tableWidgetLineModel.setItem(i, 5, cell_info_diff_y)
            cell_info_diff_y = cell_info_diff_y.clone()
            self.c_view.ui.tableWidgetNoLineModel.setItem(i, 8, cell_info_diff_y)

            diff_y_pow_2 = self.c_coefficient_model.get_diff_y_pow_2
            cell_info_diff_y_pow_2 = QTableWidgetItem(str(round(diff_y_pow_2[i], 5)))
            self.c_view.ui.tableWidgetLineModel.setItem(i, 6, cell_info_diff_y_pow_2)
            cell_info_diff_y_pow_2 = cell_info_diff_y_pow_2.clone()
            self.c_view.ui.tableWidgetNoLineModel.setItem(i, 9, cell_info_diff_y_pow_2)

    @staticmethod
    def set_line_edit_value(line_edit: QLineEdit, value: float):
        line_edit.setText(str(round(value, 11)))
