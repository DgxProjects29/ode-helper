#print(get_wf_derivative("2x^2", 3))
#print(solset_to_derivate(['2', '3'], 1))
#print(get_wfdet_of_param_variation(['2x', '3x^2', 'e^x'], "3x", 3))
from ode3_utils import get_problem_url
import solvers_utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

PATH = "C:\\Users\\User\\Documents\\Diego\\chromedriver.exe"
TIMEOUT = 15
CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument("--log-level=3")

RESULTS_SECTION_SELECTOR = "._2GT4c"

def start_program():

    driver = webdriver.Chrome(PATH, options = CHROME_OPTIONS)

    try:
        
        driver.get(get_problem_url("D[x]"))
        result_section = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, RESULTS_SECTION_SELECTOR)
            )
        )
        print("Lookin...")
        res = solvers_utils.find_wf_res(driver, result_section, 0)
        print(res)
        x = input("END")
        
    except TimeoutException:
        print("Could not find the element in the time specified")
    finally:
        driver.quit()

if __name__ == '__main__':

    start_program()