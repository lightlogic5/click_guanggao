from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Keys,ActionChains
from selenium.webdriver.common.by import By
import time,re,sys,os,argparse
import requests
from update_proxy import open_browser,update_browser,clean_borswer_cache

from goto import goto

parser = argparse.ArgumentParser(description='点广告应用')

parser.add_argument("--method", '-m', choices=['add', 'multiple'], help='选择启动浏览器个数')
parser.add_argument("--ads_id", '-i', type=str ,help='填写浏览器的id号，以启动对应浏览器环境')

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
args = parser.parse_args()


def get_driver(chrome_driver_url,debug_url):
    chrome_options = Options()
    driver_url =chrome_driver_url
    debug_addr = debug_url
    chrome_options.add_experimental_option("debuggerAddress", debug_addr)
    driver = webdriver.Chrome(service=Service(driver_url), options=chrome_options)
    return driver

# 关闭浏览器多余页面
def clean_borswer(driver):
    pages = driver.window_handles
    original_window = driver.current_window_handle
    # 循环执行，直到找到一个新的窗口句柄
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            driver.close()
            driver.switch_to.window(original_window)
        else:
            continue
    

def search_advertisement(driver,key_word,key_url):
    # 查询广告
    Sponsored = f"//span[@class and contains(text(), 'Sponsored')]/following-sibling::div//span[{key_url.strip()}]/ancestor::div/a"
    elements = driver.find_elements(By.XPATH, Sponsored)
    for k,i in enumerate(elements):
        ActionChains(driver)\
            .move_to_element_with_offset(i, 0, -50)\
            .key_down(Keys.CONTROL)\
            .click(i)\
            .key_up(Keys.CONTROL)\
            .perform()
        time.sleep(1)
    
def search(driver,key_word,key_url):
    clean_borswer(driver)
    driver.get("https://www.google.com")
    time.sleep(2)
    driver.find_element(By.XPATH,'//textarea[@aria-label="Search" or @aria-label="Pesquisar" or @aria-label="Buscar"]').send_keys(key_word)
    ActionChains(driver)\
        .key_down(Keys.ENTER)\
        .key_up(Keys.ENTER)\
        .perform()
    time.sleep(2)  
    for i in range(5):
        search_advertisement(driver,key_word,key_url)
        time.sleep(2)
        try:
            next_page_button = driver.find_element(By.XPATH,'//span[text()="Next"]')
        except:
            next_page_button = 0
        if next_page_button !=0:
            ActionChains(driver)\
                .click(next_page_button)\
                .perform()
        else:
            break   
    pages = driver.window_handles
    for k,v in enumerate(pages):
        driver.switch_to.window(v)
        time.sleep(1)

def get_keyword():
    file_path = os.path.join(BASE_DIR,"关键字.txt")
    with open(file_path, "r") as f:
        all_text = f.read()
    count,key_word,key_url = re.split(r'={4,}', all_text)
    cleaned_key_word = [item.strip() for item in key_word.split('\n') if item.strip() != '']
    cleaned_key_url = [item.strip() for item in key_url.split('\n') if item.strip() != '']
    cleaned_key_url = ' or '.join(f"contains(text(), '{keyword}')" for keyword in cleaned_key_url)
    return count,cleaned_key_word,cleaned_key_url

browser_id = args.ads_id
count,s_word,key_url = get_keyword()

@goto
def main():
    for c in range(int(count)):
        for i in s_word:
            label .end
            pd_while = 0
            while pd_while==0:
                pd_while = update_browser(browser_id)  # 此处只要返回的是0就是失败，要一直重试
                if pd_while==0:
                    print("更新浏览器失败，正在重试...")
                else:
                    updated_browser = pd_while
                    break
                time.sleep(1)
            chrome_driver_url,debug_url = updated_browser
            driver = get_driver(chrome_driver_url,debug_url)
            try:
                search(driver,i,key_url)
            except:
                print(f"查找关键字:{i}失败，重试...")
                # 查找关键字失败，就要关闭再重新建浏览器环境，再重新查找
                time.sleep(1)
                driver.quit()
                close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + browser_id
                is_close = -1
                while is_close != 0:       
                    try:
                        res_close = requests.get(close_url,timeout=(5, 5)).json()
                        is_close = res_close["code"]
                    except:
                        continue
                else:
                    print("关闭浏览器成功121 ",res_close["code"])
                time.sleep(2)
                goto .end

            time.sleep(1)
            driver.quit()
            close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + browser_id
            is_close = -1
            while is_close != 0:       
                try:
                    res_close = requests.get(close_url,timeout=(5, 5)).json()
                    is_close = res_close["code"]
                except:
                    continue
            else:
                print("关闭浏览器成功121 ",res_close["code"])
            time.sleep(2)
        clean_borswer_cache()
        time.sleep(2)

main()