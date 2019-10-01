#encoding=utf-8
import sys
import requests
from bs4 import BeautifulSoup
import time


# PTT_Beauty_URL = 'https://www.ptt.cc/bbs/Beauty/index.html'


def context_crawl_push(URL, Count_array, like, boo):
    
    resp = requests.get(url=URL, cookies={'over18': '1'})
    resp.encoding = 'utf-8'
    assert str(resp.status_code)[0] == "2", "status_code Error" + str(resp.status_code)
    soup = BeautifulSoup(resp.text, 'html.parser')

    tag = soup.html.find_all('span', {'class', 'push-tag'})
    user = soup.html.find_all('span', {'class', 'push-userid'})

    for i in range(0, len(tag)):
        if tag[i].text == '推 ':
            like += 1
        elif tag[i].text == '噓 ':
            boo += 1

        is_exist = False
        for j in range(0, len(Count_array)):
            if Count_array[j][0] == user[i].text:

                if tag[i].text == '推 ':
                    Count_array[j][1] += 1
                elif tag[i].text == '噓 ':
                    Count_array[j][2] += 1
                    
                is_exist = True
                break

        if is_exist is False:
            if tag[i].text == '推 ':
                Count_array.append([])
                Count_array[len(Count_array)-1].append(user[i].text)
                Count_array[len(Count_array)-1].append(1)
                Count_array[len(Count_array)-1].append(0)
            elif tag[i].text == '噓 ':
                Count_array.append([])
                Count_array[len(Count_array)-1].append(user[i].text)
                Count_array[len(Count_array)-1].append(0)
                Count_array[len(Count_array)-1].append(1)

    return Count_array, like, boo


def context_crawl_popular(URL, Array, count):
    resp = requests.get(url=URL, cookies={'over18': '1'})
    resp.encoding = 'utf-8'
    assert str(resp.status_code)[0] == "2", "status_code Error" + str(resp.status_code)
    soup = BeautifulSoup(resp.text, 'html.parser')

    count += 1
    a_tag = soup.html.find_all('a')
    list_img = [".jpg", ".jpeg", ".png", ".gif"]

    for i in range(0, len(a_tag)):
        for j in range(0, 4):
            if a_tag[i].get("href").endswith(list_img[j]):
                Array.append(a_tag[i].get("href"))
                break


    return Array, count

def keyword_element(URL, Array, keyword):

    resp = requests.get(url=URL, cookies={'over18': '1'})
    resp.encoding = 'utf-8'
    assert str(resp.status_code)[0] == "2", "status_code Error" + str(resp.status_code)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    text = soup.get_text().split("--\n※ 發信站")[0].split("返回看板")[1]
    if keyword in text:
        a_tag = soup.html.find_all('a')
        list_img = [".jpg", ".jpeg", ".png", ".gif"]

        for i in range(0, len(a_tag)):
            for j in range(0, 4):
                if a_tag[i].get("href").endswith(list_img[j]):
                    Array.append(a_tag[i].get("href"))
                    break

    return Array

### Create new dict ###
def dict_create():
    small_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
    big_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    number_letter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    Dict = {}

    for i in range(len(small_letter)):
        Dict[small_letter[i]] = []
    for i in range(len(big_letter)):
        Dict[big_letter[i]] = []
    for i in range(len(number_letter)):
        Dict[number_letter[i]] = []

    return Dict

# 2324 2758
def crawl():
    
    # 開啟檔案
    all_articles = open("all_articles.txt", "w", encoding="utf-8")
    all_popular = open("all_popular.txt", "w", encoding="utf-8")
    
    # first
    PTT_Beauty_URL = 'https://www.ptt.cc/bbs/Beauty/index2324.html'
    resp = requests.get(url=PTT_Beauty_URL, cookies={'over18': '1'})
    resp.encoding = 'utf-8'
    assert str(resp.status_code)[0] == "2", "status_code Error" + str(resp.status_code)
    soup = BeautifulSoup(resp.text, 'html.parser')
    div_section = soup.html.find_all('div', {'class', 'r-ent'})

    for i in range(0, len(div_section)):
        if div_section[i].find('a') != None:

            title = div_section[i].find('a').text
            
            if "[公告]" in title:
                continue

            href = 'https://www.ptt.cc' + div_section[i].find('a').get("href")
            date = div_section[i].find('div', {'class': 'date'}).text.replace(' ', '').replace('/', '') 
            
            if date[0:2] == '12':
                continue
            
            # article part
            string = date + ',' + title + ',' + href
            
            print(string, file=all_articles)

            # popular part
            if div_section[i].find('span', {'class': 'hl'}) != None:
                # print(div_section[i].find('span', {'class': 'hl'}).text)
                if div_section[i].find('span', {'class': 'hl'}).text == '爆':
                    print(string, file=all_popular)
            
    

    for page in range(2325, 2758):

        PTT_Beauty_URL = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
        resp = requests.get(url=PTT_Beauty_URL, cookies={'over18': '1'})
        resp.encoding = 'utf-8'
        assert str(resp.status_code)[0] == "2", "status_code Error" + str(resp.status_code)
        soup = BeautifulSoup(resp.text, 'html.parser')
        div_section = soup.html.find_all('div', {'class', 'r-ent'})

        for i in range(0, len(div_section)):
            if div_section[i].find('a') != None:

                title = div_section[i].find('a').text
                
                if "[公告]" in title:
                    continue

                href = 'https://www.ptt.cc' + div_section[i].find('a').get("href")
                date = div_section[i].find('div', {'class': 'date'}).text.replace(' ', '').replace('/', '') 

                string = date + ',' + title + ',' + href

                # article part
                print(string, file=all_articles)

                # popular part
                if div_section[i].find('span', {'class': 'hl'}) != None:
                    # print(div_section[i].find('span', {'class': 'hl'}).text)
                    if div_section[i].find('span', {'class': 'hl'}).text == '爆':
                        print(string, file=all_popular)
                

    # last
    PTT_Beauty_URL = 'https://www.ptt.cc/bbs/Beauty/index2758.html'
    resp = requests.get(url=PTT_Beauty_URL, cookies={'over18': '1'})
    resp.encoding = 'utf-8'
    assert str(resp.status_code)[0] == "2", "status_code Error" + str(resp.status_code)
    soup = BeautifulSoup(resp.text, 'html.parser')
    div_section = soup.html.find_all('div', {'class', 'r-ent'})

    for i in range(0, len(div_section)):
        if div_section[i].find('a') != None:

            title = div_section[i].find('a').text
            
            if "[公告]" in title:
                continue

            href = 'https://www.ptt.cc' + div_section[i].find('a').get("href")
            date = div_section[i].find('div', {'class': 'date'}).text.replace(' ', '').replace('/', '') 
            
            if len(date) == 3:
                continue

            string = date + ',' + title + ',' + href
            
            # article part
            print(string, file=all_articles)
            
            # popular part
            if div_section[i].find('span', {'class': 'hl'}) != None:
                # print(div_section[i].find('span', {'class': 'hl'}).text)
                if div_section[i].find('span', {'class': 'hl'}).text == '爆':
                    print(string, file=all_popular)

    


    # 關閉檔案
    all_articles.close()
    all_popular.close()




def push(start_date, end_date):

    ## Open file
    fp = open('all_articles.txt', "r", encoding='utf-8')
    line = fp.readline()
    Count_array = []
    all_like = 0
    all_boo = 0
    
    # Dict = dict_create()

    # count = 0
    ## 用 while 逐行讀取檔案內容，直至檔案結尾
    while line:
        line = line.encode('utf-8').decode('utf-8-sig')
        # start_time = time.time()
        if line[3] == ',':
            number = int(line[0:3])
        else:
            number = int(line[0:4])

        if number >= start_date and number <= end_date:
            # count += 1
            # href = 0
            for i in range(0, len(line)):
                if line[len(line)-i-1] == ',':
                    Count_array, all_like, all_boo = context_crawl_push(line[len(line)-i:len(line)-1], Count_array, all_like, all_boo)
                    break

            # print(number)
        line = fp.readline()


    # print(Count_array)

    # Count_array.sort(key=lambda x: (-x[1], x[0]))
    # print(Count_array[0:10])

    # Count_array.sort(key=lambda x: (-x[2], x[0]))
    # print(Count_array[0:10])

    # print(all_like, all_boo)
        
    fp.close()


    # output txt
    push_txt = open("push[{}-{}].txt".format(start_date, end_date), "w", encoding="utf-8")
    print("all like: " + str(all_like), file=push_txt)
    print("all boo: " + str(all_boo), file=push_txt)

    Count_array.sort(key=lambda x: (-x[1], x[0]))
    for i in range(0, 10):
        print("like #" + str(i) + ": " + Count_array[i][0] + " " + str(Count_array[i][1]), file=push_txt)

    Count_array.sort(key=lambda x: (-x[2], x[0]))
    for i in range(0, 10):
        print("boo #" + str(i) + ": " + Count_array[i][0] + " " + str(Count_array[i][2]), file=push_txt)

    
def popular(start_date, end_date):
    ## Open file
    fp = open('all_popular.txt', "r", encoding='utf-8')
    line = fp.readline()
    count = 0
    Array = []

    ## 用 while 逐行讀取檔案內容，直至檔案結尾
    while line:
        line = line.encode('utf-8').decode('utf-8-sig')
        # start_time = time.time()
        if line[3] == ',':
            number = int(line[0:3])
        else:
            number = int(line[0:4])

        if number >= start_date and number <= end_date:
            
            for i in range(0, len(line)):
                if line[len(line)-i-1] == ',':
                    Array, count = context_crawl_popular(line[len(line)-i:len(line)-1], Array, count)
                    break

        line = fp.readline()
    
    # print(Array)
    popular_txt = open("popular[{}-{}].txt".format(start_date, end_date), "w", encoding="utf-8")    


    print("number of popular articles: {}".format(count), file=popular_txt)
    for i in range(0, len(Array)):
        print(Array[i], file=popular_txt)

    fp.close()

def keyword(keyword, start_date, end_date):

    # Open file
    fp = open('all_articles.txt', "r", encoding='utf-8')
    line = fp.readline()
    Array = []
        
    # 用 while 逐行讀取檔案內容，直至檔案結尾
    while line:
        line = line.encode('utf-8').decode('utf-8-sig')

        if line[3] == ',':
            number = int(line[0:3])
        else:
            number = int(line[0:4])

        if number >= start_date and number <= end_date:
            
            for i in range(0, len(line)):
                if line[len(line)-i-1] == ',':
                    Array = keyword_element(line[len(line)-i:len(line)-1], Array, keyword)
                    break

        line = fp.readline()

    keyword_txt = open("keyword({})[{}-{}].txt".format(keyword, start_date, end_date), "w", encoding="utf-8")
    for i in range(0, len(Array)):
        print(Array[i], file=keyword_txt)
    

if __name__ == '__main__':
    start_time = time.time()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'crawl':
            crawl()
        elif sys.argv[1] == 'push':
            if len(sys.argv) == 4:
                push(int(sys.argv[2]), int(sys.argv[3]))
            else:
                print("wrong push input")
        elif sys.argv[1] == 'popular':
            if len(sys.argv) == 4:
                popular(int(sys.argv[2]), int(sys.argv[3]))
            else:
                print("wrong push input")
        elif sys.argv[1] == 'keyword':
            if len(sys.argv) == 5:
                keyword(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
            else:
                print("wrong push input")
        else:
            print("argv[1] error")
    else:
        print("Please input argv")
    
    print("--- %s seconds ---" % (time.time() - start_time))