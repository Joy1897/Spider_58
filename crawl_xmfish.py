import time
import requests
from pyquery import PyQuery as pQ

url_start = 'http://fangzi.xmfish.com/web/search_hire.html?h=&hf=&ca=5920'
url_end = '&r=&s=&a=&rm=&f=&d=&tp=&l=0&tg=&hw=&o=&ot=0&tst=0&page='
xm_fish_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
local_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取时间
filename = local_time + 'xm_fish.csv'


def generate_url():
    urls = []

    # 思明可访问页数134
    for i in range(134):
        urls.append(url_start + "1" + url_end + str(i+1))

    # 湖里可访问页数134
    for i in range(134):
        urls.append(url_start + "2" + url_end + str(i+1))

    # 集美可访问页数38
    for i in range(38):
        urls.append(url_start + "3" + url_end + str(i+1))

    # 海沧可访问页数34
    for i in range(34):
        urls.append(url_start + "4" + url_end + str(i+1))

    # 翔安可访问页数16
    for i in range(16):
        urls.append(url_start + "5" + url_end + str(i+1))

    # 同安可访问页数8
    for i in range(8):
        urls.append(url_start + "6" + url_end + str(i+1))

    # 杏林可访问页数15
    for i in range(15):
        urls.append(url_start + "8" + url_end + str(i+1))

    return urls


def parse_href(current_url):
    response = requests.get(url=current_url, headers=xm_fish_head)
    if response.status_code == 200:
        response.encoding = "UTF-8"
        doc = pQ(response.text)
        #  在进行正式的爬取之前先将页面的加密内容破解
        lis = doc('#select_tab2 > ul > li')  # 通过JS路径匹配要爬取的元素
        for value in lis.items():
            name = value('div.list-word > h3 > a').text()
            name = " ".join(name.split('，'))
            info = value('div.list-word > span.list-attr').text()
            floor = info.split('第')[1].split('层')[0]
            add = value('div.list-word > span.list-addr').text()
            village = value('div.list-word > span.list-addr > em:nth-child(1) > a').text()
            district = add.split('[')[1].split('-')[0]
            rent = value('div.list-word > span.list-price').text().split('元/月')[0]
            branded = value('div.list-word > div > span > i').text()
            is_branded = branded.find('品牌公寓')
            if is_branded == -1:  # 不是品牌公寓
                info = " ".join(info.split('朝'))
                rent_type = info.split()[0]
                house_type = info.split()[1]
                layout = info.split()[2]
                square = info.split()[3].split('平米')[0]
                direction = info.split()[4]
                trim_type = info.split()[5]
                update_time = value('div.list-word > span:nth-child(7)').text()
                sub_page_url = 'http://fangzi.xmfish.com' + value('div.list-word > h3 > a').attr('href')
                response_sub = requests.get(url=sub_page_url, headers=xm_fish_head)
                if response_sub.status_code == 200:
                    response_sub.encoding = "UTF-8"
                    sub_doc = pQ(response_sub.text)
                    describe = sub_doc('#info1 > div.bd > div').text()
                    describe = "".join(describe.split())
                    describe = " ".join(describe.split('，'))
                    describe = " ".join(describe.split(','))
                    with open(filename, 'a', encoding='UTF-8') as f:
                        f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}\n '
                                .format(name, rent_type, house_type, layout, square, floor, direction, trim_type,
                                        add, district, rent, village, describe, update_time))
                    with open('for_the_word_cloud.csv', 'w', encoding='utf-8') as f:
                        f.write('{0},{1}\n'.format(name, describe))
            else:
                info = " ".join(info.split('第'))
                rent_type = info.split()[0]
                house_type = info.split()[1]
                layout = info.split()[2]
                square = info.split()[3].split('平米')[0]
                direction = 'null'
                trim_type = 'null'
                update_time = value('div.list-word > span.list-square').text()
                sub_page_url = 'http://fangzi.xmfish.com' + value('div.list-word > h3 > a').attr('href')
                response_sub = requests.get(url=sub_page_url, headers=xm_fish_head)
                if response_sub.status_code == 200:
                    response_sub.encoding = "UTF-8"
                    sub_doc = pQ(response_sub.text)
                    describe = sub_doc('body > div.bck > div > div > div.col-md-5').text()
                    describe = " ".join(describe.split('\n'))
                    describe = " ".join(describe.split('，'))
                    describe = " ".join(describe.split(','))
                    describe = "".join(describe.split('房源描述'))
                    describe = "".join(describe.split('收起'))
                    with open(filename, 'a', encoding='UTF-8') as f:
                        f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}\n '
                                .format(name, rent_type, house_type, layout, square, floor, direction, trim_type,
                                        add, district, rent, village, describe, update_time))
                    with open('for_the_word_cloud.csv', 'w', encoding='utf-8') as f:
                        f.write('{0},{1}\n'.format(name, describe))


def main():
    urls = generate_url()
    if urls:
        for url in urls:
            parse_href(url)


if __name__ == '__main__':
    main()
