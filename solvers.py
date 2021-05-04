from ode3_utils import SolverTemplate, get_problem_url
import solvers_utils
import re
import time

# There is no validation
class InvalidInputException(Exception):
    """ invalid input provided by the user """
    pass

class HomogeneousODEArgBase(SolverTemplate):

    """
    parse ode in the following list of dicts

    {
        sign: +|-
        coef: <coef>
        order
    }

    """

    ode_pattern = r"([-+]){0,1}([^-+\s ]*)y('*)"

    def __init__(self, ode):
        self.ode = ode
        self.terms = []

    def parse_ode(self):
        work_ode = self.ode.replace(' ', '') # clean spaces
        matchs = re.finditer(self.ode_pattern, work_ode)
        for match in matchs:
            sign = match.group(1) or '+'
            coef = match.group(2) or '1'
            order = len(match.group(3)) or 0
            self.terms.append({
                'sign': sign,
                'coef': coef,
                'order': order
            })
    
    def print_ode_header(self):
        print(f"ODE:  {self.ode}")

class CauchyEuler(HomogeneousODEArgBase):

    digit_coef_pattern = r"(\d+)x*"

    def __init__(self, ode):
        super().__init__(ode)

    def parse_input(self):
        self.parse_ode()
        #also you could check if it is a CauchyEuler ODE
    
    def init_solver(self):
        self.title = "CauchyEuler ODE"
        self.aux_equa = ""
        self.msolutions = []
        self.create_aux_ecua()
        self.func_steps = [self.find_solutions]

    def print_header(self):
        
        self.print_ode_header()
        line2 = f"AUX EQUA:  {self.aux_equa}\n"
        print(line2)
    
    def finish_solver(self):
        line1 = f"AUX EQUA solutions {self.msolutions}\n"
        print(f"{line1}\n\n")

    def create_aux_ecua(self):

        is_first_term = True
        aux_terms = []
        for term in self.terms:
            mcoef = self.get_aux_mcoef(term['order'])
            digit_coef = self.get_aux_digit_coef(term['coef'])
            aux_sign = self.get_aux_sign(term['sign'], is_first_term)
            aux_terms.append(f"{aux_sign}{digit_coef}{mcoef}")
            is_first_term = False

        self.aux_equa = "".join(aux_terms)

    def get_aux_mcoef(self, order):
        m_coef = "".join([f"(m - {str(i)})" for i in range(order)])
        return m_coef.replace("(m - 0)", "m")

    def get_aux_digit_coef(self, coef):
        match = re.match(self.digit_coef_pattern, coef)
        if not match:
            return '1'
        return match.group(1) 

    def get_aux_sign(self, sign, is_first_term):
        if is_first_term and sign == '+':
            return ''
        
        return f" {sign} "

    def find_solutions(self):
        print("find the results of the auxiliar equation")

        self.driver.get(get_problem_url(f"{self.aux_equa} = 0"))
        result_section = solvers_utils.get_result_section(self.driver)

        print("Loading solutions...", end='\n')
        time.sleep(5)
        print("Solutions Loaded", end='\n\n')
        
        imgs = result_section.find_elements_by_class_name("_3vyrn")
        sol_dict = {}
        for index_key, img_res in enumerate(imgs, start=1):
            res = img_res.get_attribute("alt").replace(" ", "")
            sol_dict[index_key] = res
            print(f"{index_key}.  {res}")

        input_message = "\nChoose the solutions separated by a dash:  "
        solution_string = str(input(input_message))
        print()
        sols = solution_string.split('-')
        self.msolutions = [sol_dict[int(sol_index)] for sol_index in sols]

class ParameterVariationN(SolverTemplate):

    def __init__(self, args):
        self.fx, *self.solset = args

    def init_solver(self):
        self.title = "Parameter Variation"
        self.u_derivatives = []
        self.u_solutions = []
        self.wroskian = ""
        self.func_steps = [
            self.get_wroskian, 
            self.find_u_derivatives, 
            self.find_solutions
        ]

    def print_header(self):

        line1 = f"f(x):  {self.fx}\n"
        line2 = f"Solutions set:  {self.solset}\n"
        print(f"{line1}{line2}")
    
    def finish_solver(self):
        line1 = f"U Derivatives: {self.u_derivatives}\n"
        line2 = f"U Solutions: {self.u_solutions}"
        print(f"{line1}{line2}\n\n")

    def get_wroskian(self):
        print("find the wroskian of the sol set")

        solset_string = ",".join(self.solset)
        self.driver.get(get_problem_url(f"wronskian({{{solset_string}}},x)"))

        print("Looking for the wroskian...", end='\n')
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.wroskian = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            1
        )
        
        print(f"Wroskian found:  {self.wroskian}", end='\n')

    def find_u_derivatives(self):
        print("find 'u' derivatives")

        w_det_querys = []

        for u_number in range(1, len(self.solset) + 1):
            w_det_querys.append(solvers_utils.get_wfdet_of_param_variation(
                self.solset, self.fx, u_number
            ))
        
        for i, w_det in enumerate(w_det_querys, start = 1):
            self.driver.get(get_problem_url(w_det))
            result_section = solvers_utils.get_result_section(self.driver)
            res = solvers_utils.find_wf_res(
                self.driver, 
                result_section, 
                1, 
                sleep_time = 6
            )
            res_extra = f"({res})/({self.wroskian})"
            input(f"u{i}' found: {res_extra},  Press Enter to Continue:")
            self.u_derivatives.append(res_extra)

    def find_solutions(self):
        print("find 'u' solutions")

        wf_integrals = []

        for uderi in self.u_derivatives:
            wf_integrals.append(f"integrate[{uderi}]")
        
        for i, wf_integral in enumerate(wf_integrals, start = 1):
            self.driver.get(get_problem_url(wf_integral))
            result_section = solvers_utils.get_result_section(self.driver)
            res = solvers_utils.find_wf_res(
                self.driver, 
                result_section, 
                0, 
                sleep_time = 6
            )
            input(f"u{i} found: {res},  Press Enter to Continue:")
            self.u_solutions.append(res)