from abc import ABC

from PyQt5.QtWidgets import QMainWindow
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

from view.lab_canvas import LabCanvas
from utility.lab_meta import LabMeta
from model.lab_model import LabModel
from utility.lab_observer import LabObserver
from design.MainWindow import Ui_MainWindow


class LabView(QMainWindow, LabObserver, ABC, metaclass=LabMeta):
    def __init__(self, in_controller, in_model: LabModel, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.v_controller = in_controller
        self.v_model = in_model

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonSettingsStart.clicked.connect(self.v_controller.simulate)
        self.ui.pushButtonEvalCoefficients.clicked.connect(self.v_controller.eval_coefficients)

        # self.ui.dblSpinBoxSrcReqLambdaInt.valueChanged.connect(self.v_controller.srcReqLambdaIntChange)
        # self.ui.dblSpinBoxSrcReqLambdaTime.valueChanged.connect(self.v_controller.srcReqLambdaTimeChange)
        # self.ui.dblSpinBoxServiceReqMuInt.valueChanged.connect(self.v_controller.srcReqMuIntChange)
        # self.ui.edgeB.valueChanged.connect(self.v_controller.srcReqMuTimeChange)

        #self.canvas = LabCanvas(self.get_figure([], []))
        #self.nav_bar = NavigationToolbar2QT(self.canvas, self.ui.widgetPlot)
        #self.ui.vLayoutPlot.addWidget(self.canvas)
        #self.ui.vLayoutPlot.addWidget(self.nav_bar)

        self.t_list = list()
        self.load_list = list()

        self.v_model.add_observer(self)

    def model_is_changed(self):
        self.t_list = list()
        self.load_list = list()
        # print('here 1')
        for data in self.v_model.simulation():
            self.ui.dblSpinBoxResultsIntensitySrcPractice.setValue(data[0])
            self.ui.dblSpinBoxResultsIntensityServicePractice.setValue(data[1])
            self.ui.dblSpinBoxResultsLoadPractice.setValue(data[2])

            t_all = data[2] / (data[0] * (1 - data[2]))
            t_wait = pow(data[2], 2) / (data[0] * (1 - data[2]))

            if t_wait < 0:
                t_wait = 0
                t_all = 1 / data[1]

            self.t_list.append(t_all)
            self.load_list.append(data[2])
            self.t_list.sort()
            self.load_list.sort()
            if data[3] == 100:
                print(f'Обработано заявок: {data[3]} | Текущее время: {round(data[4], 2)} | '
                      f'Время ожидания: {round(t_wait, 2)} | Время пребывания: {round(t_all, 2)}')
            #self.ui.statusbar.showMessage(f'Обработано заявок: {data[3]} | Текущее время: {round(data[4], 2)} | '
             #                             f'Время ожидания: {round(t_wait, 2)} | Время пребывания: {round(t_all, 2)}')

        #     x = [1, 0, 0, 0, 0, 0, 0]
        #     d = self.ui.dblSpinBoxLevelsVarLambdaTo.value() - self.ui.dblSpinBoxLevelsVarLambdaFrom.value()
        #     x[1] = (self.ui.dblSpinBoxSrcReqLambdaInt.value() - self.ui.dblSpinBoxLevelsVarMuFrom.value()) * 2 / d - 1
        #     d = self.ui.dblSpinBoxLevelsVarMuTo.value() - self.ui.dblSpinBoxLevelsVarMuFrom.value()
        #     x[2] = (self.ui.dblSpinBoxServiceReqMuInt.value() - self.ui.dblSpinBoxLevelsVarMuFrom.value()) * 2 / d - 1
        #     d = self.ui.dblSpinBoxLevelsVarSigmaTo.value() - self.ui.dblSpinBoxLevelsVarSigmaFrom.value()
        #     x[3] = (self.ui.edgeA.value() - self.ui.dblSpinBoxLevelsVarSigmaFrom.value()) * 2 / d - 1
        #     x[4] = x[1] * x[2]
        #     x[5] = x[1] * x[3]
        #     x[6] = x[2] * x[3]

        # import numpy
        # print(f'Линейная модель: {self.v_controller.c_coefficient_model.line_function(numpy.array(x[:4]))}')
        # print(f'Нелинейная модель: {self.v_controller.c_coefficient_model.function(numpy.array(x))}')

        #self.ui.statusbar.showMessage(f'Результат модели: {self.v_controller.c_coefficient_model.function(numpy.array(x))}')

        #ЗДЕСЬ РАСКОМЕНТЬ ЧТОБЫ БЫЛ ГРАФИК
        #self.update_image()

    def update_image(self):
        #self.ui.vLayoutPlot.removeWidget(self.canvas)
        #self.ui.vLayoutPlot.removeWidget(self.nav_bar)
        self.canvas = LabCanvas(self.get_figure(self.load_list, self.t_list))
        #self.nav_bar = NavigationToolbar2QT(self.canvas, self.ui.widgetPlot)
        #self.ui.vLayoutPlot.addWidget(self.canvas)
        #self.ui.vLayoutPlot.addWidget(self.nav_bar)

    def get_figure(self, x, y):
        from matplotlib import pyplot

        fig, axes = pyplot.subplots(dpi=100, facecolor='white', figsize=(20, 15))


        axes.set_title('Время пребывания/загрузка')
        axes.plot(x, y)
        axes.grid(True)

        #fig.savefig('grafek4.png', dpi=100)
        #fig.show()
        #pyplot.show()

        return fig
