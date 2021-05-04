import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

MOUSE_OVER_SCRIPT = """

event = document.createEvent("HTMLEvents");
event.initEvent("mouseover", true, true);
event.eventName = "mouseover";
document.querySelectorAll("._8J16o")[{pos}].dispatchEvent(event)

"""

TIMEOUT = 15
RESULTS_SECTION_SELECTOR = "._2GT4c"
RESULT_CONTAINER_SELECTOR = "._8J16o"

WOLFRAM_URL = "https://www.wolframalpha.com/input/?i={expression}"

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

def get_problem_url(expression):
    parsed_exp = urllib.parse.quote(expression)
    return WOLFRAM_URL.format(expression = parsed_exp)

def get_wf_derivative(func, order):
    if order == 0:
        return func
    xres = ",x"*order
    return f"D[{func}{xres}]"


def get_wfset_from_list(l):
    join_list = ",".join(l)
    return f"{{{join_list}}}"


def solset_to_derivate(solset, order):
    return list(map(lambda sol: get_wf_derivative(sol, order), solset))


def get_wfdet_of_param_variation(solset, fx, u_number):

    rows = []

    order = len(solset)
    for i in range(order):
        row_list = solset_to_derivate(solset, i)
        if i == order - 1:
            row_list[u_number - 1] = fx
        else:
            row_list[u_number - 1] = '0'
        rows.append(get_wfset_from_list(row_list))
    wf_det_query = ",".join(rows)
    return f"Det[{{{wf_det_query}}}]"


def find_wf_res(driver, result_section, pos, sleep_time=5):
    time.sleep(sleep_time)
    driver.execute_script(MOUSE_OVER_SCRIPT.format(pos=pos))
    try:
        a_element = result_section.find_element_by_css_selector(
            f"{RESULT_CONTAINER_SELECTOR} a"
        )
        res = a_element.get_attribute("title")
    except NoSuchElementException:
        imgs = result_section.find_elements_by_class_name("_3vyrn")
        res = imgs[pos].get_attribute("alt").replace(" ", "")
        res = res[res.find("=") + 1:]
    return res


def get_result_section(driver):
    result_section = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, RESULTS_SECTION_SELECTOR)
        )
    )
    return result_section