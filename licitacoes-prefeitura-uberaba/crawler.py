import requests
import logging
import sys
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException    

i = int(sys.argv[1])
page = int(sys.argv[2])

year = 2020 - i
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_experimental_option("prefs", {
        "download.default_directory": "/home/rennan/Documents/repositories/mpmg/licitacoes-prefeitura-uberaba/" + str(year),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        "plugins.always_open_pdf_externally": True
})
options.add_argument('window-size=1920x1080')

destination_dir = "/home/rennan/Documents/repositories/mpmg/licitacoes-prefeitura-uberaba/" + str(year)
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

url = "http://www.uberaba.mg.gov.br/portal/conteudo,29557"
try:
    while True:
        driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
        driver.get(url)
        time.sleep(5)
        driver.switch_to_frame(driver.find_element_by_id("iframeLicitacoes"))
        time.sleep(5)
        el = driver.find_element_by_xpath("//select[@class='aling-left margin-top margin-bottom border']")
        el = el.find_elements_by_tag_name('option')
        el[i].click()
        time.sleep(5)

        try:
            print(page)
            elem = driver.find_element_by_xpath("//select[@class='align-left margin-right border']")
            elem = elem.find_elements_by_tag_name('option')
            print(len(elem))
            elem[page].click()
            time.sleep(5)
        except Exception as e:
            print(e)
            break
        item = 0
        while True:
            try:
                print(item)
                elem = driver.find_elements_by_xpath("//img[@class='align-left cursor']")
                elem[item].click()
                time.sleep(1)
            except Exception as e:
                print(e)
                break
            item+=1
        with open(destination_dir + "/page-" + str(page + 1) + ".html", "w") as f:
            f.write(driver.page_source)
        page+=1
        time.sleep(4)
        driver.close()
except:
    driver.close()