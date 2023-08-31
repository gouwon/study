#!/home/gouwon/venv/py_venv3.9/bin/python
#-*- coding: utf-8 -*-

## usage ##
## crontab
## every mon(1)-fri(5) 08:45 executed
## 45 8 * * 1,2,3,4,5 export DISPLAY=:0 && /home/gouwon/venv/py_venv3.9/bin/python /home/gouwon/development/02.Project/001.Auto_Commute/prt-auto_commute.py prt-auto_commute.toml > /home/gouwon/auto_commute.log 2>&1
## egasu ##

## ref ##
## https://hithot.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80%EC%9D%84-%EC%9C%84%ED%95%9C-%ED%8C%8C%EC%9D%BC-%EC%84%A4%EC%B9%98-%EC%9A%B0%EB%B6%84%ED%88%AC
## fer ##


from time import sleep
from random import randrange
import sys
import os
from datetime import datetime
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import toml
import telegram

CNFIG_FL = 'prt-auto_commute.toml' if len(sys.argv) != 2 else sys.argv[1]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CNFG_PTH = os.path.join(BASE_DIR, CNFIG_FL)

with open(CNFG_PTH, "r", encoding='utf8') as f:
    cfg_data = toml.load(f)

def auto_commute(user_info, url='https://ngwx.ktbizoffice.com/LoginN.aspx?compid=iteyes'):
    service = Service(executable_path='/home/gouwon/development/02.Project/001.Auto_Commute/chromedriver-linux64/chromedriver')
    chrome_options = Options()
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    TextUserID = driver.find_element(By.ID, 'TextUserID')
    TextPassword = driver.find_element(By.ID, 'TextPassword')
    LoginButton = driver.find_element(By.ID, 'LoginButton')

    TextUserID.send_keys(user_info['user_id'])
    TextPassword.send_keys(user_info['user_pw'])
    LoginButton.send_keys(Keys.RETURN)
    sleep(5)

    tabs = driver.window_handles
    for idx, window in enumerate(tabs):
        if idx == 0:
            continue
        driver.switch_to.window(window)
        driver.close()
    driver.switch_to.window(tabs[0])
    sleep(5)

    timeinterval_to_execute = randrange(1, 10) * 60

    sleep(timeinterval_to_execute)
    js_result = driver.execute_script(
        """
        var isOff = false;
        var ul = document.querySelector('#mainFrame').contentWindow.document.querySelector('#subtdde08 > iframe').contentWindow.document.querySelector('#tdResultList > ul');

        disIN = document.querySelector('#mainFrame').contentWindow.document.querySelector('#subtd38ce > iframe').contentWindow.document.querySelector('#disIN')

        for (var li of ul.children) {
            if (li.textContent.search("휴일|%s") > 0) {
                isOff = true;
            }
        }

        if (!isOff) {
            if (disIN.textContent === '출근입력') {
                disIN.click();
                console.log('isOff >> ' + isOff);
            }
        }
        return isOff;
        """ % (user_info['user_nm'])
    )
    sleep(3)

    result = 'success' if js_result else 'fail'

    driver.quit()

    return result

def send_noti_by_telegram(tele_msg='기본값입니다.'):
    token = cfg_data['telegram']['token']
    chat_id = cfg_data['telegram']['chat_id']
    bot = telegram.Bot(token=token)
    asyncio.run(bot.send_message(chat_id=chat_id, text=tele_msg))
    sleep(3)

if __name__ == '__main__':
    url = cfg_data['url']

    for user_info in cfg_data['user_info']:
        commute_result = auto_commute(user_info, url)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tele_msg = f'출근 하였습니다.\n 실행완료시간: {now}' if commute_result == 'success' else f'출근 하지 못 했습니다.\n 실행완료시간: {now}'
        send_noti_by_telegram(tele_msg=tele_msg)
