class LaplaceParser:

    laplace_type = ""
    laplace_command = ""

    def __init__(self, match, laplace_expression):
        self.match = match
        self.laplace_expression = laplace_expression
        # after applying the property
        self.new_laplace = ""
        self.new_expression = ""

    def apply_property(self):
        pass
    
    def get_new_expression(self):
        return self.new_expression

    def get_new_laplace(self):
        return f"{self.laplace_type}{{{self.new_laplace}}}"

    def get_wolfram_query(self):
        return f"{self.laplace_command.format(nl = self.new_laplace)}"

        

class Translation1(LaplaceParser):

    laplace_type = "L"
    laplace_command = "LaplaceTransform[{nl}, t, s]"

    def apply_property(self):
        s_sign = self.match.group(1) or '+'
        a = self.match.group(2) or '1'

        oppositive_s_sing = '+' if s_sign == '-' else '-'         

        translation = f"s -> s {oppositive_s_sing} {a}"

        self.new_laplace = self.laplace_expression.replace(self.match[0], "1")
        self.new_laplace = self.new_laplace.replace('1t', 't')

        self.new_expression = f"L{{{self.new_laplace}}} | {translation}"


class Translation1Inverse:
    pass

class Translation2(LaplaceParser):

    laplace_type = "L"
    laplace_command = "LaplaceTransform[{nl}, t, s]"

    def apply_property(self):
        a = self.match.group(1)
        euler_exp = f"e^(-{a}s)"
        #u_pattern = fr"(\d*)\(t-{a}\)"
        exp_coef = self.laplace_expression.replace(self.match[0], "1")
        self.new_laplace = exp_coef.replace("t", f"(t+{a})")
        self.new_laplace = self.new_laplace.replace('*1', '')
        self.new_laplace = self.new_laplace.replace(')1', ')')

        self.new_expression = f"{euler_exp} * L{{{self.new_laplace}}}"
        

class Translation2Inverse(LaplaceParser):

    laplace_type = "L^-1"
    laplace_command = "InverseLaplaceTransform[{nl}, s, t]"
    
    def apply_property(self):
        a = self.match.group(1) or '1'
        u_expression = f"u(t-{a})"        
        translation = f"t -> t - {a}"
        
        self.new_laplace = self.laplace_expression.replace(self.match[0], "1")

        self.new_expression = \
            f"{u_expression} * L^-1{{{self.new_laplace}}} | {translation}"
