import base64
import io
import re
import requests.adapters
from retrying import retry
from pyquery import PyQuery as pQ
from fontTools.ttLib import TTFont

urlStart = 'https://xm.58.com/chuzu/pn7/?PGTID=0d3090a7-0025-e721-cb23-e34b7c4e7ffe&ClickID=1'
tc_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def get_num(response):  # 破解字体加密
    base64_str = re.search("base64,(.*?)'\)", response.text).group(1)
    bin_data = base64.b64decode(base64_str)
    font = TTFont(io.BytesIO(bin_data))
    best_cmap = font['cmap'].getBestCmap()
    new_map = dict()
    for key in best_cmap.keys():
        value = int(re.search(r'(\d+)', best_cmap[key]).group(1)) - 1
        key = hex(key)
        new_map[key] = value
    response_ = response.text
    for key, value in new_map.items():
        key_ = key.replace('0x', '&#x') + ';'
        if key_ in response_:
            response_ = response_.replace(key_, str(value))
    return response_


@retry(stop_max_attempt_number=3)
def url_to_context(page_url):
    response = requests.get(url=page_url, headers=tc_head)
    print(response.text)
    if response and response.status_code == 200:
        response.encoding = "UTF-8"
        response_ = get_num(response)
        context = pQ(response_)
        return context
    else:
        print('fail')


def parse_href(page_url):
    doc = url_to_context(page_url)
    #  在进行正式的爬取之前先将页面的加密内容破解
    lis = doc('body > div.mainbox > div > div.content > div.listBox > ul > li')  # 通过JS路径匹配要爬取的元素
    i = 0
    for value in lis.items():
        i += 1
        # 开始访问各个房源URL下的详细信息
        sub_page_url = value('div.des > h2 > a').attr('href')
        # if sub_page_url is None:
        #     continue
        if value('div.des').text().find('来自品牌公寓') == -1:
            house_type = 'not an apart'
        else:
            house_type = 'apart'
        if house_type == 'apart':
            print(house_type)
    print(i)


def main():
    parse_href(urlStart)


if __name__ == '__main__':
    main()
