import sys
from request_proccesor import InvalidRequestException, PersonalStopException, get_solver_class
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

PATH = "data/chromedriver.exe"
CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument("--log-level=3")

def start_program(solver_class):

    driver = webdriver.Chrome(PATH, options = CHROME_OPTIONS)
    
    solver_class.parse_input()
    solver_class.init()
    solver_class.set_driver(driver)
        
    try:
        start_process = input("START PROCESS [y/n]:  ")

        steps = solver_class.get_func_steps()

        if start_process == 'n':
            raise PersonalStopException("Stop program by the will of the user")
        print('Start:  ', end='\n\n')

        for step in steps:
            
            step()

            continue_process = input("CONTINUE PROCESS [y/n]:  ")

            if continue_process == 'n':
                raise PersonalStopException(
                    "stop program by the will of the user"
                )
            print()

        solver_class.finish_solver()

    except TimeoutException:
        print("Could not find the element in the time specified")
    except PersonalStopException as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == '__main__':

    _, req, *args = sys.argv
    try:
        solver_class = get_solver_class(req, args)
        start_program(solver_class)
    except InvalidRequestException as ir:
        print(ir)