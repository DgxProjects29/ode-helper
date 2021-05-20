from solvers.solvers4 import CompactFunction, LaplaceLineal, LaplaceProperty
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
    else:
        raise InvalidRequestException(
            "It looks like you didn't specify the request or does not exit"
        )