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
