""" class ParameterVariation2:

    def __init__(self, args):
        self.fx, *self.solset = args

    def parse_input(self):
        pass

    def create_steps(self):
        self.steps = [
            {
                "descp": "find the wroskian of the sol set",
                "wolfram": "wronskian({{{solset_string}}},x)",
                "process_func": self.get_wroskian,
                "dkwargs": {"solset_string": "sol1,sol2.."}
            },
            {
                "descp": "find u1",
                "wolfram": "integral of ({derivative_u1})",
                "process_func": self.find_u1,
                "dkwargs": {"derivative_u1": "u1'"},
                "use_driver": True
            },
            {
                "descp": "find u2",
                "wolfram": "integral of ({derivative_u2})",
                "process_func": self.find_u2,
                "dkwargs": {"derivative_u2": "u2'"},
                "use_driver": True
            },
        ]

    def init_solver(self):
        self.create_steps()
        self.u1 = ""
        self.u2 = ""
        self.wroskian = ""

    def get_problem_info(self):

        base_header = get_problem_header("ParameterVariation Orden 2")
        line1 = f"f(x):  {self.fx}\n"
        line2 = f"Solutions set:  {self.solset}\n"
        problem_info = f"{base_header}{line1}{line2}"

        return problem_info
    
    def get_steps(self):
        return self.steps

    def get_initial_kwargs(self):
        return {"solset_string": ",".join(self.solset)}
    
    def get_final_message(self, final_kwargs):
        line1 = f"U solutions\n"
        line2 = f"u1 = {self.u1}\n"
        line3 = f"u2 = {self.u2}\n"
        yp = f"({self.solset[0]}*{self.u1}) + ({self.solset[1]}*{self.u2})";
        line4 = f"Yp = {yp}\n"
        line5 = f"Simplify wolfram link: {get_problem_url(yp)}\n"
        return f"{line1}{line2}{line3}{line4}{line5}\n\n"

    def get_wroskian(self, results_section):
        print("Looking for the wroskian...", end='\n')
        time.sleep(5)

        imgs = results_section.find_elements_by_class_name("_3vyrn")
        wroskian_img = imgs[1]
        wroskian = wroskian_img.get_attribute("alt").replace(" ", "")
        self.wroskian = wroskian
        
        print(f"Wroskian found:  {wroskian}", end='\n')
        du1 = self.get_derivative_of_u1()
        print(f"next query:  {du1}", end='\n\n')

        return {'derivative_u1': du1}

    def find_u1(self, results_section, driver):
        print("Looking for the integral solution...", end='\n')
        time.sleep(5)

        driver.execute_script(MOUSE_OVER_SCRIPT)
        a_element = results_section.find_element_by_css_selector("._8J16o a")
        integral_result = a_element.get_attribute("title")

        #clean integral
        self.u1 = integral_result
        print(f"u1 found:  {integral_result}", end='\n')
        du2 = self.get_derivative_of_u2()
        print(f"next query:  {du2}", end='\n\n')

        return {'derivative_u2': du2}

    def find_u2(self, results_section, driver):
        print("Looking for the integral solution...", end='\n')
        time.sleep(5)

        driver.execute_script(MOUSE_OVER_SCRIPT)
        a_element = results_section.find_element_by_css_selector("._8J16o a")
        integral_result = a_element.get_attribute("title")

        #clean integral
        self.u2 = integral_result
        print(f"u2 found:  {integral_result}", end='\n\n')

        return {}

    def get_derivative_of_u1(self):
        return f"(-1 * {self.solset[1]} * {self.fx})/({self.wroskian})"

    def get_derivative_of_u2(self):
        return f"({self.solset[0]} * {self.fx})/({self.wroskian})" """