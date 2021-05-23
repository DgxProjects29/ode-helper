from solvers import solvers_utils

class ExactPartialDerivative(solvers_utils.SolverTemplate):

    def __init__(self, m_function, n_function):
        self.m_function = m_function 
        self.n_function = n_function 

    def init_solver(self):
        self.title = "Exact Partial Derivative"
        self.n_partial = ''
        self.m_partial = ''
        self.func_steps = [
            self.find_derivatives            
        ]

    def print_header(self):
        print("M(x,y) = ", self.m_function)
        print("N(x,y) = ", self.n_function)

    def finish_solver(self):
        print("Summary")
        print("δn/δx =  ", self.n_partial)
        print("δm/δy =  ", self.m_partial)
        
    def find_derivatives(self):
        print("looking for: δn/δx")
        query = solvers_utils.get_wf_derivative(self.n_function, 1)
       
        wolfram_query = solvers_utils.get_problem_url(query)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.n_partial = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            0
        )        
        print("δn/δx =  ", self.n_partial)
        
        print("looking for: δm/δy")
        query = solvers_utils.get_wf_derivative(
            self.m_function, 1, variable='y'
        )
       
        wolfram_query = solvers_utils.get_problem_url(query)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.m_partial = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            0
        )
        
        print("δm/δy =  ", self.m_partial)


class LineIntegral(solvers_utils.SolverTemplate):

    def __init__(self, param_function, fxy, integral_range):
        self.param_function = param_function 
        self.fxy = fxy 
        self.integral_range = integral_range

    def parse_input(self):
        n = len(self.param_function)
        components = self.param_function[1:n - 1].split(',')
        self.replaced_function = self.fxy.replace('x',f"({components[0]})") \
            .replace('y',f"({components[1]})")


    def init_solver(self):
        self.title = "Line Integral"
        self.d_param_function = ''
        self.norm_d_param_function = ''
        self.integral_query = ''
        self.integral_result = ''
        self.func_steps = [
            self.compute_derivative,            
            self.compute_norm,            
            self.compute_integral,            
        ]

    def print_header(self):
        print("r(t) = ", self.param_function)
        print("f(x,y) = ", self.fxy)
        print("f(x(t),y(t)) = ", self.replaced_function)
        print("range = ", self.integral_range)

    def compute_derivative(self):
        print("looking for r'(t)")
        query = solvers_utils.get_wf_derivative(
            self.param_function, 1, variable='t'
        )
       
        wolfram_query = solvers_utils.get_problem_url(query)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.d_param_function= solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            0
        )        
        print("r'(t) =  ", self.d_param_function)
        
    def compute_norm(self):
        print("looking for || r'(t) ||")
        query = f'Norm[{self.d_param_function}]'
       
        wolfram_query = solvers_utils.get_problem_url(query)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.norm_d_param_function = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            1
        )        
        print("|| r'(t) || =  ", self.norm_d_param_function)

    def compute_integral(self):        
        integral_expression = \
            f"({self.replaced_function}) * {self.norm_d_param_function}"

        print("computing integral expression:  ", integral_expression)

        self.integral_query = \
            f"integrate[{integral_expression}, {{t,{self.integral_range}}}]"

        wolfram_query = solvers_utils.get_problem_url(self.integral_query)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.integral_result = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            0
        )        
        print("result =  ", self.integral_result)
        
    
    def finish_solver(self):
        print("Summary")
        print("r'(t) =  ", self.d_param_function)        
        print("|| r'(t) || =  ", self.norm_d_param_function)
        print("integral query: ", self.integral_query)
        print("integral result =  ", self.integral_result)
    

class FieldLineIntegral(solvers_utils.SolverTemplate):
  
    def __init__(self, param_function, fxy, integral_range):
        self.param_function = param_function 
        self.fxy = fxy 
        self.integral_range = integral_range

    def parse_input(self):
        n = len(self.param_function)
        components = self.param_function[1:n - 1].split(',')
        self.replaced_function = self.fxy.replace('x', f"({components[0]})") \
            .replace('y',f"({components[1]})")
    
    def init_solver(self):
        self.title = "Field Line Integral"
        self.d_param_function = ''
        self.dot_product = ''
        self.integral_query = ''
        self.integral_result = ''
        self.func_steps = [
            self.compute_derivative,            
            self.compute_dot_product,            
            self.compute_integral,            
        ]

    def print_header(self):
        print("r(t) = ", self.param_function)
        print("F(x,y) = ", self.fxy)
        print("F(r(t)) = ", self.replaced_function)
        print("range = ", self.integral_range)

    def compute_derivative(self):
        print("looking for r'(t)")
        query = solvers_utils.get_wf_derivative(
            self.param_function, 1, variable='t'
        )
       
        wolfram_query = solvers_utils.get_problem_url(query)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.d_param_function= solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            0
        )        
        print("r'(t) =  ", self.d_param_function)

    def compute_dot_product(self):
        print("looking for F(r(t)) * r'(t)")
        query = f'Dot[{self.d_param_function}, {self.replaced_function}]'
       
        wolfram_query = solvers_utils.get_problem_url(query)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.dot_product = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            1
        )        
        print("F(r(t)) * r'(t) =  ", self.dot_product)

    def compute_integral(self):        
        integral_expression = f"{self.dot_product} "

        print("computing integral expression:  ", integral_expression)

        self.integral_query = \
            f"integrate[{integral_expression}, {{t,{self.integral_range}}}]"

        wolfram_query = solvers_utils.get_problem_url(self.integral_query)
        self.driver.get(wolfram_query)
        
        result_section = solvers_utils.get_result_section(self.driver)
        self.integral_result = solvers_utils.find_wf_res(
            self.driver, 
            result_section, 
            0
        )        
        print("result =  ", self.integral_result)
    
    
    def finish_solver(self):
        print("Summary")
        print("r'(t) =  ", self.d_param_function)                
        print("F(r(t)) * r'(t) =  ", self.dot_product)
        print("integral query: ", self.integral_query)
        print("integral result =  ", self.integral_result)


class PotentialFunction(solvers_utils.SolverTemplate):

    def __init__(self, components):
        self.components = components

    def parse_input(self):
        self.components = self.components.split(',')

    
    def init_solver(self):
        self.title = "Potential Function"
        self.default_variables = ['x', 'y', 'z',]
        self.partial_integrals = [] 
        self.func_steps = [
            self.find_derivatives            
        ]

    def print_header(self):
        print("partial derivatives: ", self.components)

    def find_derivatives(self):
        for i, component in enumerate(self.components):
            variable = self.default_variables[i]
            print(f"looking for: integral with respect to {variable}")

            query = solvers_utils.get_wf_integral(
                component, variable=variable
            )
        
            wolfram_query = solvers_utils.get_problem_url(query)
            self.driver.get(wolfram_query)
            
            result_section = solvers_utils.get_result_section(self.driver)
            partial_integral = solvers_utils.find_wf_res(
                self.driver, 
                result_section, 
                0
            )

            print(f"result of {variable}:  ", partial_integral)
            self.partial_integrals.append(partial_integral)
         
    def finish_solver(self):        
        for i, partial_integral in enumerate(self.partial_integrals):
            variable = self.default_variables[i]            
            print(f"integrate with respect to {variable}:  ", partial_integral)
        
