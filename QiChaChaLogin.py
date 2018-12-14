# -*- coding:utf-8 -*-
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from matplotlib.font_manager import FontProperties
from pylab import array, imshow, ginput, show, axis
import matplotlib.pyplot as plt
from PIL import Image

USERNAME = "xxxxxxxxx"
PASSWORD = "xxxxxxxxx"


class QiChaChaLogin(object):
    def __init__(self):
        firefox_profile = webdriver.FirefoxProfile()
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        firefox_profile.update_preferences()
        self.driver = webdriver.Firefox(firefox_options=options,firefox_profile=firefox_profile)
        self.driver.set_window_size(1920, 1080)

    def cookie_validity(self):
        pass

    def get_login(self):
        self.driver.get('https://www.qichacha.com/user_login')
        self.driver.find_element_by_xpath('//*[@id="normalLogin"]').click()

    def get_sliding(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="nc_1_n1z"]')))
        finally:
            dragger = self.driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            action = ActionChains(self.driver)
            action.click_and_hold(dragger).perform() 
            try:
                action.move_by_offset(350, 0).perform() 
            except:
                pass
            action.reset_actions()
            sleep(3)

    def get_img_code(self):
        cap = self.driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]').text
        self.driver.save_screenshot("c.png")
        img_element = self.driver.find_element_by_xpath('//*[@id="nc_1_clickCaptcha"]/div[2]/img')  
        location = img_element.location
        size = img_element.size
        rangle = (int(location['x']), int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) 
        i = Image.open("c.png")
        frame4 = i.crop(rangle)
        frame4.save('b.png')
        return cap, img_element

    def get_coordinate(self,cap):
        font = FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf', size=14)
        im = array(Image.open('b.png'))
        axis('off')
        plt.title(cap, fontproperties=font)
        imshow(im)
        coordinate = ginput(1)
        return coordinate

    def write_img_code_coordinate(self, coordinate,img_element):
        x,y = coordinate[0]
        ActionChains(self.driver).move_to_element_with_offset(img_element, x, y).click().perform()

    def send_name_pwd(self):
        self.driver.find_element_by_xpath('//*[@id="nameNormal"]').send_keys(USERNAME)
        self.driver.find_element_by_xpath('//*[@id="pwdNormal"]').send_keys(PASSWORD)
        sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div[2]/form/button').click()


    def main(self):
        self.get_login()        # 访问登录页，选择密码登陆
        self.get_sliding()     # 滑动按钮，显示图片验证码
        cap, img_element = self.get_img_code()  # 获取需要选中的文字,截取图片验证码
        coordinate = self.get_coordinate(cap)          # 获取坐标
        self.write_img_code_coordinate(coordinate, img_element)    # 点击网页文字验证
        self.send_name_pwd()         # 输入用户名密码, 登陆


if __name__ == '__main__':
    QiChaChaLogin().main()
