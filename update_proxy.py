import requests,time
import random
import string,json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys,ActionChains
import sys

def generate_device_name(prefix="DESKTOP-", length=5):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    device_name = prefix + random_string
    return device_name

def get_random_proxy():
    with open('proxy_list.json', 'r') as f:
        proxy_list = json.load(f)    
    proxy = random.choice(proxy_list)
    return proxy

def get_one_proxy():				
    mainUrl  = "http://myip.lunaproxy.io/"				
    entry = 'http://{}:{}@pr.zzyku2jc.lunaproxy.net:12233'.format("user", "passwd")
    proxy = {
        'http': entry,
        'https': entry,
    }
    while True:
        try:                   
            res = requests.get(mainUrl, proxies=proxy, timeout=10)
            if res.status_code == 200:
                ip_address = res.text.split("|")[0]
                print("获取到的ip是",ip_address)
                break
            else:
                continue              
        except Exception as e:  
            print("获取代理ip失败")                 
            continue
    return ip_address

def update_browser(browser_id):
    # proxy = get_random_proxy()
    # proxy = get_one_proxy()
    # print("get_ip:",proxy)
    # username = proxy.get('username')
    # password = proxy.get('password')
    # proxy_address = proxy.get('proxy_address')
    # port = proxy.get('port')
    # proxy_address = proxy
    # port = "12233"
    cpu_core = random.choice(["2", "4", "6", "8", "default"])
    device_name = generate_device_name()
    device_memory = random.choice(["2", "4", "6", "8", "default"])
    ads_id = browser_id
    url2 = "http://local.adspower.net:50325/api/v1/user/update"
    payload = {
    "user_id": ads_id,
    "domain_name":"https://www.google.com/",
    "fingerprint_config": {
        "webrtc": "forward",
        "random_ua" :{"ua_browser":["chrome"],"ua_version":["125","126"],"ua_system_version":["Windows 10"]},
        "client_rects":"1",
        "media_devices":"1",
        "screen_resolution":"random",
        "hardware_concurrency":cpu_core,
        "device_memory":device_memory,
        "client_rects":"1",
        "device_name_switch":"2",
        "device_name":device_name,
        "webrtc": "forward",
        "automatic_timezone":"1",
        "automatic_timezone": "1",
        "language": ["en-US","en"],
        "language_switch":"1",
        "location_switch":"1",
        "webgl_image":"1",
        "canvas":"1",
        "audio":"1"
        },
        "cookie":[],
        # "user_proxy_config": {
        #     "proxy_soft":"other",
        #     "proxy_type":"socks5",
        #     "proxy_host":proxy_address,
        #     "proxy_port":port,
        #     "proxy_user":username,
        #     "proxy_password":password
        # }
        "proxyid":"2"
    }
    headers = {
    'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url2, headers=headers, json=payload,timeout=10)
    except:
        return 0
    if str(response.json()["code"]) == "-1":  # 0是成功，-1是失败
        print("创建环境失败！！正在重试")
        return 0
    else:
        open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
        try:
            resp = requests.get(open_url,timeout=30).json()
            if resp["code"] != 0:   # 0是成功，-1是失败
                return 0
        except:
            return 0
        chrome_driver_url,debug_url = open_browser(resp)
        if chrome_driver_url == -1:  # 0是成功，-1是失败
            return 0
        else:
            return [chrome_driver_url,debug_url]

def clean_borswer_cache():
    url = "http://localhost:50325/api/v1/user/delete-cache"
    payload={}
    headers = {}
    response = requests.request("POST", url, headers=headers, json=payload)
    time.sleep(30)
    if response.json()["code"] == 0:
        print("清理缓存成功")

def open_browser(resp):
    if resp["code"] != 0:  # 0是成功，-1是失败
        return -1,-1
        # sys.exit()

    chrome_driver_url = resp["data"]["webdriver"]
    debug_url = resp["data"]["ws"]["selenium"]
    # chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", debug_url)
    # driver = webdriver.Chrome(service=Service(chrome_driver_url), options=chrome_options)

    return chrome_driver_url,debug_url

    """
    # 查询广告
    driver.find_element(By.XPATH,'//textarea[@aria-label="Search"]').send_keys("aaaaa")
    ActionChains(driver)\
        .key_down(Keys.Enter)\
        .key_up(Keys.Enter)\
        .perform()
    time.sleep(3)
    Sponsored = "//span[@class and contains(text(), 'Sponsored')]/following-sibling::div//span[{key_word.strip()}]/ancestor::div/a"
    elements = driver.find_elements(By.XPATH, Sponsored)
    print("获取到的可点击元素有：",len(elements))

    for k,i in enumerate(elements):
        ActionChains(driver)\
            .move_to_element_with_offset(i, 0, -50)\
            .key_down(Keys.CONTROL)\
            .click(i)\
            .key_up(Keys.CONTROL)\
            .perform()
        time.sleep(1)
    pages = driver.window_handles
    for k,v in enumerate(pages):
        driver.switch_to.window(v)
        time.sleep(1)
    # driver.quit()
    # requests.get(close_url)
    """
