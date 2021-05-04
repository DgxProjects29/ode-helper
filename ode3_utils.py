import urllib.parse

WOLFRAM_URL = "https://www.wolframalpha.com/input/?i={expression}"

def get_problem_url(expression):
    parsed_exp = urllib.parse.quote(expression)
    return WOLFRAM_URL.format(expression = parsed_exp)

class SolverTemplate:

    def set_driver(self, driver):
        self.driver = driver

    def parse_input(self):
        pass

    def init(self):
        self.func_steps = []
        self.title = "No title"
        #steps_func
        self.init_solver()
        self.print_title()
        self.print_header()

    def print_header(self):
        pass
    
    def get_func_steps(self):
        return self.func_steps

    def print_title(self):
        print(f"-------------------{self.title}-------------------\n\n")

    def finish_solver(self):
        pass

    def loop_steps(self):
        self.ste