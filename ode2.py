import urllib.parse
import sys
import textwrap
import re

WOLFRAM_URL = "https://www.wolframalpha.com/input/?i={expression}"
# "-y (-21 + 2 x + y) = 0, -x (x + 2 y - 21) = 0"
#class_img_container = "_8J16o"

def get_problem_url(expression):
    parsed_exp = urllib.parse.quote(expression)
    return WOLFRAM_URL.format(expression = parsed_exp)

def get_wroskian_url(solset):
    exp = f"wronskian({{{', '.join(solset)}}}, x)"
    results = f"query: {exp} \n\n"
    results += f"wroskinan url: {get_problem_url(exp)}"
    return results

class OrderReduccion:

    template = """
        
    Numerator = {num}
    Denominator = {dem}
    ei = integral of (num/dem)
    finalBase = {y1} * ei
        
    """

    def __init__(self, px, y1):
        self.px = px
        self.y1 = y1

    def create_urls(self):
        
        num = "e^(integral of (-1* {px}))".format(px = self.px)
        dem = "({y1})^2".format(y1 = self.y1)

        self.num_url = get_problem_url(num)
        self.dem_url = get_problem_url(dem)

        #Cannot compute

        ei = "integral of ({num}/{dem})".format(
            num = num,
            dem = dem
        )
        
        self.external_integral_url = get_problem_url(ei)

        self.final_url = "{y1} * {ei}".format(
            y1 = self.y1, 
            ei = self.external_integral_url
        )

    
    def get_results(self):

        results = self.template.format(
            num = self.num_url,
            dem = self.dem_url,
            y1 = self.y1,
        )

        return textwrap.dedent(results)

class CheckSolutionSet:
    
    #Simplify (D[#, x, x, x] - 6D[#, x, x] + 11D[#, x] - 6#)& @ (e^(2x))
    diff_template = "D[#, {nx}]"
    exp_template = "Simplify ({diff_ode})& @ ({sol})"

    def __init__(self, ode, solset ) -> None:
        self.ode = ode
        self.solset = solset

    def create_urls(self):
        
        self.parse_ode()
        self.results = ""
        self.results += f"ODE: {self.ode} \n"
        self.results += f"DIFF ODE: {self.diff_ode} \n\n"
        for i, sol in enumerate(self.solset, start=1):
            expression = self.exp_template.format(
                diff_ode = self.diff_ode,
                sol = sol
            )
            self.results += f"Check sol {i} {get_problem_url(expression)} \n"

        self.results += f"\ncheck wroskian {get_wroskian_url(self.solset)}"

    def get_results(self):
        return self.results


    def parse_ode(self):
        """ ignore_chars = [' ', '+', '-']
        for ic in ignore_chars:
            self.ode.replace(ic, '') """
        #.*?
        pattern = r"y(')+"
        matches = re.finditer(pattern, self.ode)
        self.diff_ode = self.ode
        for match in matches:
            prima_form = match[0]
            n = len(prima_form) - 1
            diff_form = self.diff_template.format(nx = ('x, ' * n).strip(', '))
            self.diff_ode = self.diff_ode.replace(prima_form, diff_form)

        self.diff_ode = self.diff_ode.replace("y", "#")

class CoefConst:

    def __init__(self, ode):
        self.ode = ode
        self.aux_equa = ""

    def parse_ode(self):
        terms = []
        # pattern = r"\d*y(')*"
        tempode = self.ode.replace(' ', '')
        pattern = r"([+]|[-])*\d*y(')*"
        matches = re.finditer(pattern, tempode)
        for match in matches:
            term = match[0]
            coef, primes = term.split('y')
            exponent = len(primes)
            terms.append(f"{coef}m^{exponent}")
        aux_equa = "".join(terms).replace("m^0", "")
        self.aux_equa = f"{aux_equa} = 0"

    def create_urls(self):
        
        self.parse_ode()
        solve_exp = f"solve ({self.ode} = 0)"
        self.results = f"ODE: {self.ode} url: {get_problem_url(solve_exp)}\n"
        self.results += f"Aux equea: {self.aux_equa} \n\n"

        self.results += f"url: {get_problem_url(self.aux_equa)}"

    def get_results(self):
        return self.results

class ExactODE:

    def __init__(self, path, m, n):
        self.path = path
        self.m = m
        self.n = n

    def create_urls(self):

        ode = f"{self.m}dx + {self.n}dy = 0"
        solve_exp = f"solve ({ode})"
        self.results = f"ODE: {solve_exp} url: {get_problem_url(solve_exp)} \n\n"

        self.results += "---- Check if it is exact \n"

        dmy = f"d/dy({self.m})"
        dnx = f"d/dx({self.n})"

        self.results += f"My: {dmy} url: {get_problem_url(dmy)} \n"
        self.results += f"Nx: {dnx} url: {get_problem_url(dnx)} \n\n"

        self.results += "---- If It is not exact: \n"
        self.results += f"μ(x): ( {dmy} - {dnx} ) / ( {self.n} )\n"
        self.results += f"μ(y): ( {dnx} - {dmy} ) / ( {self.m} )\n"
        self.results += f"μ: integral of e^(μ)\n\n"

        self.results += "---- Process \n"

        func_to_integrate = self.m if self.path == 'x' else self.n 
        
        func_integral = f"integral of {func_to_integrate} with respect to {self.path}"
        
        self.results += f"func integral: {func_integral} url: {get_problem_url(func_integral)} \n"
        
        func_to_derivate = self.n if self.path == 'x' else self.m 
        dwith = 'y' if self.path == 'x' else 'x' 
        note = "recuerda que al integrar queda una funcion como constante en el lado isquierdo, es lo que despejamos en la siguiente ecuacion"
        self.results += note + "\n"
        derivative = f"{func_to_derivate} = d/d{dwith}(<result of func_integral>)"

        self.results += f"base for derivative: {derivative} \n"

        final_integral = f"integral of (<result of before step>) with respect to {dwith}"

        self.results += f"base for final integral: {final_integral} \n"
    
    def get_results(self):
        return self.results


def process_request(req, args):

    if req == 'red-order':
        rd = OrderReduccion(*args)
        rd.create_urls()
        print(rd.get_results())
    elif req == "coef-const":
        cf = CoefConst(*args)
        cf.create_urls()
        print(cf.get_results())
    elif req == 'check':
        edo, *solset = args
        ck = CheckSolutionSet(edo, solset)
        ck.create_urls()
        print(ck.get_results())
    elif req == 'exact':
        exa = ExactODE(*args)
        exa.create_urls()
        print(exa.get_results())
    elif req == "w":
        print(get_wroskian_url(args))
    else:
        print("It looks like you didn't specify the request or does not exit")

# check <edo> <solution>

""" 
Documentation:

command syntaxis 

<request> <arg1> <arg2> <argn>.....

1. Order Reduction:

red-order <px> <y1>

2. Constant Coefficients:

coef-const <ode>

3.Check if a set of solutions are solutions of the ode

check <ode> <sol1> <sol2> <soln>.....

4. Exact ODE

exact <path> <m> <n>

ode format mdx + ndy = 0
path: if starts with x or y

5. Wroskian

w <sol1> <sol2> <soln>....

"""
if __name__ == '__main__':

    _, req, *args = sys.argv
    process_request(req, args) 


