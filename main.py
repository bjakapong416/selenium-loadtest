from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import threading
from time import sleep
from selenium.webdriver.common.keys import Keys


chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
# chrome_options.add_argument("start-maximized")
chrome_options.add_argument("window-size=1900,1080"); 
# chrome_options.headless = True # also works
# drivers = webdriver.Chrome(options=chrome_options)

drivers = webdriver.Chrome()

# VXNAT
username = "vam01"
password = "test01"

links = ["https://vxnat.vamstack.com/vxnat"]
handles = drivers.window_handles


def open_page(url, tab_index):
    # drivers.switch_to.window(handles[-1])

    if tab_index == 0:
        drivers.get(url)
        # drivers.get(start_url)
        # find username/email field and send the username itself to the input field
        drivers.find_element("name", "username").send_keys(username)
        # find password input field and insert password as well
        drivers.find_element("name", "password").send_keys(password)
        # click login button
        drivers.find_element("name", "login").click()
        sleep(1)
    else:

        # Create New tab
        drivers.execute_script("window.open('');")
        # Switch to the new window
        drivers.switch_to.window(drivers.window_handles[tab_index])

        drivers.get(url)
        # drivers.get(start_url)
        # find username/email field and send the username itself to the input field
        drivers.find_element("name", "username").send_keys(username)
        # find password input field and insert password as well
        drivers.find_element("name", "password").send_keys(password)
        # click login button
        drivers.find_element("name", "login").click()
        sleep(1)

    return


all_threads = []
for i in range(0, 2):
    current_thread = threading.Thread(target=open_page, args=(links[0], i,))
    all_threads.append(current_thread)
    current_thread.start()

for thr in all_threads:
    thr.join()