from viktor.parametrization import Parametrization, HiddenField


class CPTParametrization(Parametrization):
    headers = HiddenField('headers')
    measurement_data = HiddenField('measurement_data')
