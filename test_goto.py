from goto import goto
import random
import time


def update_browser():
    return random.choices([0,0,0,0,0,0,[2,1],[0,2],0,0,0,0,0], k=1)



@goto
def main():
    label .end
    pd_while = 0
    while pd_while==0:
        pd_while = update_browser()[0]  # 此处只要返回的是0就是失败，要一直重试 
        print(pd_while)
        if pd_while!=0:
            updated_browser = pd_while
            print("跳出循环，值为",updated_browser)
            break 
        time.sleep(1)  
    chrome_driver_url,debug_url = updated_browser
    print(chrome_driver_url,debug_url)
    # driver = get_driver(chrome_driver_url,debug_url)
    try:
        print("除法的值为：",debug_url/chrome_driver_url)
    except:
        print("除零错误，跳到开头重试")
        goto .end

main()