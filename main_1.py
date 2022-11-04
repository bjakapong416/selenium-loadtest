import datetime
import sys
from selenium import webdriver 
from concurrent.futures import ThreadPoolExecutor, wait
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import argparse
import xlsxwriter

# from scrapers.scraper import connect_to_base, get_driver, parse_html, write_to_file
# VXNAT
username = "vam01"
password = "test01"
num_thread = 1000

ap = argparse.ArgumentParser()
ap.add_argument("-x", "--xlsx", required=True,
	help="output xlsx")
args = vars(ap.parse_args())


workbook = xlsxwriter.Workbook(args["xlsx"])
worksheet = workbook.add_worksheet()

# def page_is_loaded(drivers):
#     print("in page_is_loaded()")
#     return drivers.find_element("id", "API-PLAYGROUND") != None

def open_page(url, number):
# def open_page(tab_index):
    # drivers.switch_to.window(handles[-1])

    # if tab_index == 0:
    

    chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("window-size=1900,1080")
    drivers = webdriver.Chrome(options=chrome_options)
    # drivers = webdriver.Chrome()

    drivers.get(url)
    # print(drivers.get(url))

    # drivers.get(start_url)
    # find username/email field and send the username itself to the input field
    # if number == 1:
    #     username = 'vam01'
    #     password = 'test01'
    # else: 
    #     username = 'admin'
    #     password = 'vamsuperadmin'

    # print(username, password)
    start_thread = time()
    # print("start time and thread num: ", number, time() )
    drivers.find_element("name", "username").send_keys(username)
    # print(1)
    # find password input field and insert password as well
    drivers.find_element("name", "password").send_keys(password)
    # print(2)
    # click login button
    drivers.find_element("name", "login").click()
    # print("finished")
    # click first project's element
    # drivers.find_element("id","API-PLAYGROUND").click()
    # print("start")
    # wait = ui.WebDriverWait(drivers, 10)
    # wait.until(page_is_loaded)
    # if drivers.find_element("name", "thumbnail_title") != None:
    #     print("thumbnail is existed")
    # # print(text)
    # else: 
    #     print("no thumbnail")
    # sleep(5)

    # sleep(60)
    # else:

    #     # Create New tab
    #     drivers.execute_script("window.open('');")
    #     # Switch to the new window
    #     drivers.switch_to.window(drivers.window_handles[tab_index])
    #     drivers.get(url)
    #     # drivers.get(start_url)
    #     # find username/email field and send the username itself to the input field
    #     drivers.find_element("name", "username").send_keys(username)
    #     # find password input field and insert password as well
    #     drivers.find_element("name", "password").send_keys(password)
    #     # click login button
    #     drivers.find_element("name", "login").click()
    drivers.quit()
    end_thread = time()
    end_thread_time = end_thread - start_thread

    worksheet.write(f'A{number}', number)
    worksheet.write(f'B{number}', end_thread_time)

    return


if __name__ == "__main__":

    # headless mode?
    headless = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "headless":
            print("Running in headless mode")
            headless = True

    # set variables
    start_time = time()
    output_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # output_filename = f"output_{output_timestamp}.csv"
    futures = []

    url = "https://vxnat.vamstack.com/vxnat"
    # scrape and crawl
    with ThreadPoolExecutor() as executor:
        for number in range(num_thread):
            print("thread nums:", number)
            number = number + 1
            futures.append(
                # executor.submit(run_process, output_filename, headless)
                executor.submit(open_page, url, number)
            )

    wait(futures)
    # open_page(url)
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Elapsed run time: {elapsed_time} seconds")
    print("add to xlsx sucessful")
    workbook.close()