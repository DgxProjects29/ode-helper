from ode2 import get_problem_url
from solvers.laplace_parsers import DerivativeLaplace, LaplaceParser, Translation1, Translation2, Translation2Inverse
from solvers import solvers_utils
import textwrap
import re

class LaplaceLineal(solvers_utils.HomogeneousODEArgBase):

    def __init__(self, ode, ft, *pvi):
        super().__init__(ode)
        self.ft = ft
        self.pvi = pvi

    def parse_input(self):
        self.parse_ode()
    
    def init_solver(self):
        self.title = "LaplaceLineal"
        self.template_laplace_equa = ""
        self.laplace_equa = ""
        self.create_template_laplace_equa()

        self.ft_laplace_transform = ""
        self.ys = ""

        self.func_steps = [
            self.find_laplace_for_ft,
            self.solving_the_equation,
            self.find_y
        ]

    def create_template_laplace_equa(self):

        equa_terms = []
        for t_index, term in enumerate(self.terms, start = 1):
            term_parts = []
            lap_term = f"s^{term['order']}Y(s)"
            term_parts.append(lap_term)

            n = term['order'] - 1
            func_term = "-y{order}(0)s^{exp}"
            for exp in range(n, -1, -1):
                order = n - exp
                term_parts.append(func_term.format(
                    exp = exp, order = "'"* order
                ))

            coef = "" if term['coef'] == '1' else term['coef']
            if term['sign'] == '+' and t_index == 1:
                sign = ''
            else:
                sign = term['sign']
            equa_terms.append(f"{sign}{coef}({''.join(term_parts)})")
        
        equa = "".join(equa_terms).replace("s^0", "") \
            .replace("s^1","s").replace("+", " + ") \
            .replace("-", " - ")
        
        self.template_laplace_equa = equa

        for y_exp in self.pvi:
            y_exp = y_exp.replace(" ", "")
            key_repl, to_repl = y_exp.split('=')
            equa = equa.replace(key_repl, to_repl)
        
        self.laplace_equa = equa.replace("Y(s)", "x").replace("(x)", "x")


    def print_header(self):    
        self.print_ode_header()
        line2 = f"LAPLACE TEMPLATE EQUA:  {self.template_laplace_equa}\n"
        line3 = f"LAPLACE EQUA:  {self.laplace_equa}\n"
        line4 = f"f(t) = {self.ft}\n"
        line5 = f"pvi = {self.pvi}\n"
        print(line2+line3+line4+line5)

    def find_laplace_for_ft(self):

        print(f"apply laplace transform to f(t): {self.ft}")
        self.ft = self.ft.replace("u","θ")
        
        self.driver.get(
            solvers_utils.get_problem_url(f"LaplaceTransform[{self.ft}, t, s]")
        )

        print("Looking for laplace transform...")
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.ft_laplace_transform = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            1
        )

        print(f"Lpt found: {self.ft_laplace_transform}")

    def solving_the_equation(self):

        print("find the solution for Y(s) (x in the expression):")
        equa = f"Solve[{self.laplace_equa} = {self.ft_laplace_transform}, x]"
        print(f"equa: {equa}")

        self.driver.get(solvers_utils.get_problem_url(equa))

        print("Looking for the solution...")
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.ys = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            1
        )

        print(f"Y(s) = {self.ys}")

    def find_y(self):

        print(f"apply inverse laplace transform to Y(s): {self.ys}")
        query = f"InverseLaplaceTransform[{self.ys}, s, t]" 
        print(f"ILpt: {query}")

        self.driver.get(solvers_utils.get_problem_url(query))

        print("Looking for the inverse laplace transform...")
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.y = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            1
        )

        print(f"y = {self.y}")

    def finish_solver(self):
        ftext = """
        Summary:

        L{{{ft}}} = {ft_laplace_transform}
        Y(s) = {ys}
        y(t) = {y}
        """
        res = textwrap.dedent(ftext.format(
            ft = self.ft,
            ft_laplace_transform = self.ft_laplace_transform,
            ys = self.ys,
            y = self.y
        ))
        print(res)

class CompactFunction(solvers_utils.SolverTemplate):

    def __init__(self, args):
        self.raw_parts = args

    def parse_input(self):
        self.parts = []
        for raw_part in self.raw_parts:
            part_function, activate_number = raw_part.replace(' ', '') \
                .split(',');
            part_item = {
                'part_function': part_function, 
                'activate_number': activate_number
            }
            self.parts.append(part_item)
     

    def init_solver(self):
        self.title = "Compact Function"
        self.create_term_parts()
        self.create_compact_function()
        self.simplified_compact_function = ""
        self.func_steps = [
            self.simplify_function            
        ]

    def create_compact_function(self):
        w_part = ' + '.join(self.term_parts)
        self.compact_function = f"{self.parts[0]['part_function']} + {w_part}"
        
    def create_term_parts(self):
        term_template = "{w_part}u(t - {an})" 
        self.term_parts = []
        n = len(self.parts)
        for i in range(1, n):
            item0 = self.parts[i - 1]
            item = self.parts[i]
            w_part = f"(({item['part_function']}) - ({item0['part_function']}))"
            an = item['activate_number']
            self.term_parts.append(term_template.format(
                w_part = w_part,
                an = an
            ))

    def print_header(self):
        for part in self.parts:
            print("Part function: ", part['part_function'])
            print("Activate number: ", part['activate_number'])
            print("----------")

        print()
        print("compact function: ", self.compact_function, end='\n\n')

    def finish_solver(self):
        print("Compact Function: ")
        print("f(t) = ", self.compact_function)
        print("f(t) = ", self.simplified_compact_function)

    def simplify_function(self):
        print("simplify function...")
       
        wolfram_query = solvers_utils.get_problem_url(self.compact_function)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.simplified_compact_function = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            1
        )


class LaplaceProperty(solvers_utils.SolverTemplate):

    property_mappers = [
        {
            'name': "Translation 1",
            'parse_class': Translation1,
            'regex_pattern': r"e\^\((-{0,1})(\w*)t\)|e\^-{0,1}t"
        },
        {
            'name': "Translation 2",
            'parse_class': Translation2,
            'regex_pattern': r"u\(t-(\w+)\)"
        },
        {
            'name': "Translation 2 Inverse",
            'parse_class': Translation2Inverse,
            'regex_pattern': r"e\^\(-(\w*)s\)|e\^-s"
        },
        {
            'name': "Laplace Derivative",
            'parse_class': DerivativeLaplace,
            'regex_pattern': r"t\^(\d+)"
        },
    ]
    
    def __init__(self, expression):
        self.expression = expression
        self.parse_class: LaplaceParser = None
        self.property_name = 'No Property Applied'

    def parse_input(self):
        self.clean_expression = self.expression \
            .replace(' ', '')
        for property_map in self.property_mappers:
            match = re.search(property_map['regex_pattern'], self.clean_expression)

            if match:
                self.parse_class = property_map['parse_class'](
                    match, self.expression
                )
                self.property_name = property_map['name']
                break

        if self.parse_class:
            self.parse_class.apply_property()

    def init_solver(self):
        self.title = self.property_name
        self.new_laplace_sol = ""
        self.func_steps = [
            self.solve_laplace_by_user            
        ]

    def create_compact_function(self):
        w_part = ' + '.join(self.term_parts)
        self.compact_function = f"{self.parts[0]['part_function']} + {w_part}"
        
    def create_term_parts(self):
        term_template = "{w_part}u(t - {an})" 
        self.term_parts = []
        n = len(self.parts)
        for i in range(1, n):
            item0 = self.parts[i - 1]
            item = self.parts[i]
            w_part = f"(({item['part_function']}) - ({item0['part_function']}))"
            an = item['activate_number']
            self.term_parts.append(term_template.format(
                w_part = w_part,
                an = an
            ))

    def print_header(self):
        print(f"expression given: {self.expression}")
        if self.parse_class:
            print(f"new expression: {self.parse_class.get_new_expression()}")

    def finish_solver(self):
        if self.parse_class:
            ftext = """
            Summary:

            your expression = {expression}
            new expression = {new_expression}
            new laplace = {new_laplace}
            new laplace expression solution = {new_laplace_sol}
            """
            res = textwrap.dedent(ftext.format(
                expression = self.expression,
                new_expression = self.parse_class.get_new_expression(),
                new_laplace = self.parse_class.get_new_laplace(),
                new_laplace_sol = self.new_laplace_sol
            ))
            print(res)
        
    def solve_laplace_by_user(self):
        if self.parse_class:
            self.parse_class.apply_property()

            print("what do you want to do?")

            ans = input(
                f"solve the new laplace expression: {self.parse_class.get_new_laplace()} [y/n]: "  
            )

            if ans == 'y':
                wolfram_url = get_problem_url(
                    self.parse_class.get_wolfram_query()
                )

                print("Looking for result...")

                self.driver.get(wolfram_url)
                result_section = solvers_utils.get_result_section(self.driver)
                self.new_laplace_sol = solvers_utils.find_wf_res(
                    self.driver, 
                    result_section, 
                    1
                )

                print(f"Found: {self.new_laplace_sol}")
        else:
            print("it look likes we couldn't found a property for this expression...")


class Convolution(solvers_utils.SolverTemplate):
    
    def __init__(self, ft, gt):
        self.ft = ft
        self.gt = gt

    def parse_input(self):
        
        new_ft = self.ft.replace('t', 'τ')
        new_gt = self.gt.replace('t', 't - τ')

        self.convolution_integral = \
            f"integrate[{new_ft} * {new_gt}, {{τ, 0, t}}]"

    def init_solver(self):
        self.title = "Convolution"
        self.convolution_result = ""
        self.func_steps = [
            self.compute_convolution_integral            
        ]
    
    def print_header(self):
        print("f(t) = ", self.ft)
        print("g(t) = ", self.gt)
        print("ci = ", self.convolution_integral)

    def compute_convolution_integral(self):
        
        wolfram_url = get_problem_url(
            self.convolution_integral.replace('τ', 'x')
        )

        print("Looking for result...")

        self.driver.get(wolfram_url)
        result_section = solvers_utils.get_result_section(self.driver)
        self.convolution_result = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            2
        )

        print(f"Found: {self.convolution_result}")
  
    def finish_solver(self):
        print("Convolution result:  ",self.convolution_result)