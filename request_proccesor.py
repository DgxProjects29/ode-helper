from solvers.calculus_solvers import ExactPartialDerivative, FieldLineIntegral, LineIntegral, PotentialFunction
from solvers.solvers4 import CompactFunction, Convolution, LaplaceLineal, LaplaceProperty
from solvers.solvers3 import CauchyEuler, ParameterVariationN

class InvalidRequestException(Exception):
    """ invalid request provided by the user """
    pass

class PersonalStopException(Exception):
    """ invalid input provided by the user """
    pass

def get_solver_class(req, args):

    if req == 'cauchy-euler':
        return CauchyEuler(*args)
    elif req == 'parameter-variation-n':
        return ParameterVariationN(args)
    elif req == 'laplace-lineal':
        return LaplaceLineal(*args)
    elif req == 'compact-function':
        return CompactFunction(args)
    elif req == 'laplace-property':
        return LaplaceProperty(*args)
    elif req == 'convolution':
        return Convolution(*args)
    elif req == 'exact-check':
        return ExactPartialDerivative(*args)
    elif req == 'line-integral':
        return LineIntegral(*args)
    elif req == 'field-line-integral':
        return FieldLineIntegral(*args)
    elif req == 'potential-func':
        return PotentialFunction(*args)
    else:
        raise InvalidRequestException(
            "It looks like you didn't specify the request or does not exit"
        )