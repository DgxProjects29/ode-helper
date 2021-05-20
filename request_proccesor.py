from solvers.solvers4 import CompactFunction, LaplaceLineal, LaplaceProperty
from solvers.solvers3 import CauchyEuler, ParameterVariationN

class InvalidRequestException(Exception):
    """ invalid request provided by the user """
    pass

class PersonalStopException(Exception):
    """ invalid input provided by the user """
    pass


""" 
Documentation:

command syntaxis 

<request> <arg1> <arg2> <argn>.....

1. Cauchy Euler:

cauchy-euler <homogeneous-ode>

2. Parameter Variation Order 2:

parameter-variation-2 <f(x)> <solset>

Examples

cauchy-euler "4x^2y'' + 17y"
cauchy-euler "x^3y''' + 5x^2y'' + 7xy' + 8y"
parameter-variation-2 "(x + 1)e^(2x)" "e^(2x)" "xe^(2x)"
parameter-variation-2 "csc(3x)/4" "cos(3x)" "sin(3x)"

3. Parameter Variation Order N:

parameter-variation-n <f(x)> <solset>

Examples

cauchy-euler "4x^2y'' + 17y"
cauchy-euler "x^3y''' + 5x^2y'' + 7xy' + 8y"
parameter-variation-n "(x + 1)e^(2x)" "e^(2x)" "xe^(2x)"
parameter-variation-n "csc(3x)/4" "cos(3x)" "sin(3x)"

laplace-lineal "y' + 3y" "13sin(2t)" "y(0)=1"
laplace-lineal "y'' - 3y' + 2y" "e^(-4t)" "y(0)=1" "y'(0)=5"
compact-function "2,0" "-1,2" "0,3"
compact-function "20t, 0" "0, 5"

laplace-property "3t*u(t-1)"
laplace-property "e^(5t)t^3"
laplace-property "e^(-2t)cos(4t)"
laplace-property "e^(-pis)/(s^2+1)"
"""
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