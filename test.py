import base64
import io
import random
import re
import requests.adapters
import time
from retrying import retry
from pyquery import PyQuery as pQ
from fontTools.ttLib import TTFont

urlStart = 'https://xm.58.com/chuzu/pn'
urlEnd = '?PGTID=0d3090a7-0025-e721-cb23-e34b7c4e7ffe&ClickID=1'
tc_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
local_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取时间
filename = local_time + '-58tc.csv'


def generate_url():
    urls = []
    for i in range(1, 71):
        urls.append(urlStart + str(i) + urlEnd)

    return urls


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
    response = requests.get(url=page_url, headers=tc_head, timeout=3)
    if response and response.status_code == 200:
        response.encoding = "UTF-8"
        response_ = get_num(response)
        context = pQ(response_)
        return context
    else:
        print('Fail to Operate!')


def parse_href(page_url):
    doc = url_to_context(page_url)
    lis = doc('body > div.mainbox > div > div.content > div.listBox > ul > li')  # 通过JS路径匹配要爬取的元素
    for value in lis.items():
        sub_page_url = value('div.des > h2 > a').attr('href')
        if sub_page_url is None:
            continue
        time.sleep(round(random.uniform(0.5, 2), 2))
        sub_doc = url_to_context(sub_page_url)
        name = sub_doc('body > div.main-wrap > div.house-title > h1').text()
        name = " ".join(name.split('，'))
        name = " ".join(name.split(','))

        rent = sub_doc('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr '
                       '> div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_ff552e > b').text()

        rent_type = sub_doc('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr '
                            '> div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-child(1) '
                            '> span:nth-child(2)').text()

        house_info = sub_doc('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr '
                             '> div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-child(2) '
                             '> span.strongbox').text()

        house_type = '普通住宅'

        layout = house_info.split()[0]

        square = house_info.split()[1]

        try:
            trim_type = house_info.split()[3]
        except IndexError:
            trim_type = 'null'

        direction_floor = sub_doc('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr '
                                  '> div.house-basic-desc > div.house-desc-item.fl.c_333 > ul '
                                  '> li:nth-child(3) > span.strongbox').text()

        direction = direction_floor.split()[0]

        try:
            floor = direction_floor.split()[1].split('层')[0]
        except IndexError:
            floor = '不明'

        village = sub_doc('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr '
                          '> div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-child(4) '
                          '> span:nth-child(2) > a').text()
        village = " ".join(village.split())

        address = sub_doc('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr '
                          '> div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-child(5) '
                          '> span:nth-child(2)').text()
        address = " ".join(address.split())

        district = sub_doc('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr '
                           '> div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-child(5) '
                           '> span:nth-child(2) > a:nth-child(1)').text()

        describe = sub_doc('body > div.main-wrap > div.house-detail-desc > div.main-detail-info.fl '
                           '> div.house-word-introduce.f16.c_555 > ul > li:nth-child(2) > span.a2').text()
        describe = "".join(describe.split())
        describe = " ".join(describe.split('，'))
        describe = " ".join(describe.split(','))

        update_time = sub_doc('body > div.main-wrap > div.house-title > p').text().split()[0]

        with open(filename, 'a', encoding='UTF-8') as f:
            f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}\n '
                    .format(name, rent_type, house_type, layout, square, floor, direction, trim_type,
                            address, district, rent, village, describe, update_time))
            time.sleep(round(random.uniform(0.5, 2), 2))


def main():
    # with open(filename, 'w', encoding='UTF-8') as f:
    #     f.write('房源名称,租赁种类,房源类型,房源户型,房源面积,房源楼层,房源朝向,'
    #             '装修等级,房源地址,行政区划,房源描述,房源租金,所在小区,更新时间\n')
    urls = generate_url()
    if urls:
        for href in urls:
            parse_href(href)
            print('  [+]  ' + href)


if __name__ == '__main__':
    main()
