import requests
from bs4 import BeautifulSoup
from os import makedirs
from shutil import rmtree


url = 'https://tw.stock.yahoo.com/d/i/rank.php?t={}&e={}&n=100'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

chType = {    
    'tse': ['市-熱門股', '市-漲幅', '市-跌幅', '市-價差', '市-成交價', '市-成交值'], 
    'otc': ['櫃-熱門股', '櫃-漲幅', '櫃-跌幅', '櫃-價差', '櫃-成交價', '櫃-成交值']
}
tType = ['vol', 'up', 'down', 'pdis', 'pri', 'amt']


#TODO: crawl failed
def getToday(): #'109/01/01'
    path = url.format('vol', 'tse')
    request = requests.get(path, headers=headers)
    return BeautifulSoup(request.text, 'lxml').select('table')[2].text[10:23].replace(" ", '')

def rank100(tType, tseORotc, isTest=False):
    if(isTest):
        request = ''
        with open('./test/test-file.html', 'r', encoding='utf-8') as f:
            request = f.read()
        return str(BeautifulSoup(request, 'lxml').select('table')[2])
    request = requests.get(url.format(tType, tseORotc), headers=headers)
    request.encoding = 'Big5-hkscs'
    return str(BeautifulSoup(request.text, 'lxml').select('table')[2])

def mkdirs(path):
    try:
        makedirs(path)
        print(f'[DEBUG]make dirs:', path)
    except FileNotFoundError as e:
        print(f'[WARN]{e}')
    except FileExistsError:
        print(f"[WARN]{path}/ already exists.")
        exit(0)

def loadFile(path):
    with open(path, 'r', encoding='utf-8', newline='') as file:
        return file.read()

def get(tseORotc):
    allContent = ''
    todayHTML = f'{todayPath}/{tseORotc}.html'

    #get all table
    for t, c in zip(tType, chType[tseORotc]):
        allContent = allContent + rank100(t, tseORotc) + '\n<hr>'
        print(f'[DEBUG]{c}')

    #create tse.html & otc.html
    post = loadFile('./posts/post.html')
    with open(todayHTML, 'w', encoding='utf-8', newline='') as file:
        file.write(post.format(title=tseORotc, body=allContent))
    print(f'[DEBUG]create {todayHTML}')

def createTodayIndex():
    todayHTML = f'{todayPath}/index.html'
    index = loadFile('./posts/index.html')
    with open(todayHTML, 'w', encoding='utf-8', newline='') as file:
        file.write(index.format(title=today))
    print(f'[DEBUG]create {todayHTML}')

def splitToDict(s):
    return {
        'ym': s[:6], #109/01
        'y': s[:3]   #109
    }

def removeYearOrMonthDir(yORm, tail, prev):
    if(int(tail.replace('/', '')) >= int(prev.replace('/', ''))):
        return
    else:
        rmtree(f'./src/{tail}/')
        print(f'[DEBUG]remove tail {yORm} dir')

def removeTailFileAndDir(soup):   #109/01/02
    tail = soup.select('#d9')[0].string
    prev = soup.select('#d8')[0].string
    tailDict = splitToDict(str(tail))
    prevDict = splitToDict(str(prev))

    #remove file(day dir)
    if(str(tail) != 'None'):
        rmtree(f'./src/{tail}/', ignore_errors=True)
        print('[DEBUG]remove tail day dir')
    else:
        return
    #remove month dir
    removeYearOrMonthDir('month', tailDict['ym'], prevDict['ym'])
    #remove year dir
    removeYearOrMonthDir('year', tailDict['y'], prevDict['y'])

def assignTagAttr(tag, string, href):
    tag['href'] = href
    if(str(string) != 'None'):
        tag.string = str(string)

def renewSrcIndex(soup, path):
    #id="1~9"
    for i in range(9, 1-1, -1):
        prevTag = soup.select(f'#d{i-1}')[0]
        thisTag = soup.select(f'#d{i}')[0]
        assignTagAttr(thisTag, prevTag.string, prevTag['href'])
    #id="0"
    assignTagAttr(soup.select('#d0')[0], today, path)
    #id="today"
    assignTagAttr(soup.select('#today')[0], today, path)
    return soup

def renewSrcIndexAndSubdir(today):
    srcIndex = './src/index.html'
    soup = BeautifulSoup(loadFile(srcIndex), 'lxml')
    d0Tag = soup.select('#d0')[0]

    #avoid duplicate renew
    if(d0Tag.string == today):
        print(f'[DEBUG]avoid duplicate renew {srcIndex}')
        return

    removeTailFileAndDir(soup)
    soup = renewSrcIndex(soup, f'./{today}/index.html')

    #override
    with open(srcIndex, 'w', encoding='utf-8', newline='') as file:
        file.write(str(soup))


if __name__ == '__main__':

    today = getToday()
    todayPath = f'./src/{today}'
    mkdirs(todayPath)

    get('tse')
    get('otc')

    createTodayIndex()
    renewSrcIndexAndSubdir(today)