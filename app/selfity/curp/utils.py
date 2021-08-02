import requests
import csv
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


class Bot:
    def __init__(self, name, middle_name, last_name, birthday, gender, entity):
        self.driver = webdriver.Remote("http://selenium-hub:4444/wd/hub",
                                        DesiredCapabilities.FIREFOX)
        self.url = 'https://www.gob.mx/curp/'
        self.name = name
        self.middle_name = middle_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.entity = entity

    def get_web(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def audioToText(self, mp3Path):
        audioToTextDelay = 10
        self.driver.execute_script('''window.open("","_blank");''')
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('https://speech-to-text-demo.ng.bluemix.net/')
        delayTime = 10
        # Upload file
        time.sleep(1)
        # Upload file
        time.sleep(1)
        root = self.driver.find_element_by_id('root').find_elements_by_class_name(
            'dropzone _container _container_large')
        btn = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
        btn.send_keys(
            'C:/Users/AbdulBasit/Documents/google-captcha-bypass/1.mp3')
        # Audio to text is processing
        time.sleep(delayTime)
        # btn.send_keys(path)
        # Audio to text is processing
        time.sleep(audioToTextDelay)
        text = self.driver.find_element(By.XPATH,
                                   '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name(
            'span')
        result = " ".join([each.text for each in text])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return result


    def set_input_wait(self, by, input_element='', val='', time_input=2):
        def predicate(driver):
            try:
                if time_input >= 0 and val != "":
                    username_element = WebDriverWait(
                        self.driver,
                        time_input
                    ).until(
                        EC.presence_of_element_located((by, input_element))
                    )
                    username_element.send_keys(val)
            except Exception as ex:
                error = "set_input_wait {0} >> {1}".format(input_element, ex)
                return False
            else:
                return True
        return predicate

    def get_curp(self):
        element = self.driver.find_elements_by_xpath(
            '/html/body/div[2]/main/div/div/div[1]/section/div/div/div/form/div[1]/div/ul/li[2]/a')
        element[0].click()
        WebDriverWait(self.driver, timeout=900).until(
            self.set_input_wait(By.ID, 'nombre', self.name)
        )
        WebDriverWait(self.driver, timeout=900).until(
            self.set_input_wait(By.ID, 'primerApellido', self.middle_name)
        )
        WebDriverWait(self.driver, timeout=900).until(
            self.set_input_wait(By.ID, 'segundoApellido', self.last_name)
        )
        self.driver.find_element_by_xpath(
            '//*[@id="diaNacimiento"]/option[text()="{}"]'.format(
                self.birthday.day)).click()
        self.driver.find_element_by_xpath(
            '//*[@id="mesNacimiento"]/option[text()="{}"]'.format(
                self.birthday.month)).click()
        WebDriverWait(self.driver, timeout=900).until(
            self.set_input_wait(By.ID, 'selectedYear', self.birthday.year)
        )
        self.driver.find_element_by_xpath(
            '//*[@id="sexo"]/option[text()="{}"]'.format(self.gender)).click()
        self.driver.find_element_by_xpath(
            '//*[@id="claveEntidad"]/option[text()="{}"]'.format(self.entity)).click()
        time.sleep(30)
        element = self.driver.find_elements_by_xpath(
            '/html/body/div[2]/main/div/div/div[1]/section/div/div/div/form/div[3]/div/div/div/div/iframe')[
            0]
        self.driver.switch_to_frame(element)
        audioBtnFound = False
        try:
            WebDriverWait(self.driver, timeout=900).until(
                self.driver.find_element_by_xpath(
                    '/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]').click()
            )
        except Exception:
            try:
                audioBtn = self.driver.find_element_by_id(
                    'recaptcha-audio-button') or self.driver.find_element_by_id(
                    'recaptcha-anchor')
                audioBtn.click()
                audioBtnFound = True
                if audioBtnFound:
                    try:
                        while True:
                            filename = '1.mp3'
                            href = self.driver.find_element_by_id(
                                'audio-source').get_attribute('src')
                            response = requests.get(href, stream=True)
                            saveFile(response, filename)
                            response = self.audioToText(
                                os.getcwd() + '/' + filename)
                            print(response)
                            self.driver.switch_to.default_content()
                            iframe = \
                            self.driver.switch_to.frame(element)
                            inputbtn = self.driver.find_element_by_id(
                                'audio-response')
                            inputbtn.send_keys(response)
                            inputbtn.send_keys(Keys.ENTER)
                            time.sleep(2)
                            errorMsg = self.driver.find_elements_by_class_name(
                                'rc-audiochallenge-error-message')[0]
                            if errorMsg.text == "" or errorMsg.value_of_css_property(
                                    'display') == 'none':
                                print("Success")
                    except Exception as e:
                        print(e)
                        print('Caught. Need to change proxy now')
                else:
                    print('Button not found. This should not happen.')
            except Exception:
                pass
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath('//*[@id="searchButton"]').click()
        data = self.driver.find_element_by_id('CURP')
        time.sleep(200)
        self.driver.stop_client()
        self.driver.close()
        self.driver.quit()
        return data
