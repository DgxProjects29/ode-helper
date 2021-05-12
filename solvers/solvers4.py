from solvers import solvers_utils
import textwrap

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
            self.find_laplace_for_fx,
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

    def find_laplace_for_fx(self):

        print(f"apply laplace transform to f(t): {self.ft}")

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


        
    
