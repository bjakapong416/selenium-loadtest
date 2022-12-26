import datetime
import sys
from selenium import webdriver 
from concurrent.futures import ThreadPoolExecutor, wait
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import argparse
import xlsxwriter
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from scrapers.scraper import connect_to_base, get_driver, parse_html, write_to_file
# VXNAT
username = "admin"
password = "admin"
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
    tms = str(datetime.datetime.now().timestamp()).split(".")[0]
    proName = f"pro_{tms}_{number}"
    subName = f"sub_{tms}_{number}"
    experName = f"exper_{tms}_{number}"
    scanName = f"scan_{tms}_{number}"

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

    start_thread = time()
    # print("start time and thread num: ", number, time() )
    drivers.find_element("name", "username").send_keys(username)
    # sleep(1)
    # print(1)
    # find password input field and insert password as well
    drivers.find_element("name", "password").send_keys(password)
    # print(2)
    # click login button
    # sleep(1)
    drivers.find_element("name", "login").click()
    
    
    ## click upload sidebar
    drivers.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/ul/li[2]/a").click()
    # sleep(1)
    # select file from file explorer
    
    ### select photo from files explorer
    uploadButton = drivers.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div[1]/input[2]")
    # print("h2")
    # sleep(1) 
    # uploadButton.click()
    uploadButton.send_keys("/home/sovatha/Downloads/dog.jpg")
    
    # sleep(1)
    ## fill project, subject, experiment, scan name

    drivers.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/form/div[1]/div[2]/span/input").send_keys(proName)
    drivers.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/form/div[2]/div[2]/span/input").send_keys(subName)
    drivers.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/form/div[3]/div[2]/span/input").send_keys(experName)
    drivers.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/form/div[4]/div[2]/span/input").send_keys(scanName)
    # sleep(2)
    drivers.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/button").click()


    # myDynamicElement = drivers.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/button")
    # print(myDynamicElement.text)
    ## wait for upload to finish
    # element = WebDriverWait(drivers, 30).until(
	#     EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/div/div/button"))
    #     ).text == "View DICOM"
    # print("element: ", element.text)

    # element = drivers.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/button")
    # print("h1")
    # WebDriverWait(drivers, 30).until(EC.presence_of_element_located(By.NAME, "viewDicom"));
    # print("h2")
    # print(drivers.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/button").text)
    while(drivers.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/button").text != "VIEWDICOM"):
        # print("uploading")
        pass

    
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

    url = "http://10.1.1.186/VxPACS/"
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