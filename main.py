import requests
from bs4 import BeautifulSoup
from os import makedirs
from shutil import rmtree, copytree
import json
from datetime import datetime


#url = 'https://tw.stock.yahoo.com/d/i/rank.php?t={}&e={}&n=100'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

chType = {    
    'TAI': ['市-熱門股', '市-漲幅', '市-跌幅', '市-價差', '市-成交價', '市-成交值'], 
    'TWO': ['櫃-熱門股', '櫃-漲幅', '櫃-跌幅', '櫃-價差', '櫃-成交價', '櫃-成交值']
}
tType = ['vol', 'up', 'down', 'pdis', 'pri', 'amt']

api_tt = ["TAI", "TWO"]
api_url = 'https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.rank;exchange={};limit=100;offset=0;period=1D;sortBy={}'
api_name = ["volume", "change-up", "change-down", "day-range", "price", "turnover"]
api_sort = ["-volume", "-changePercent", "changePercent", "-dayHighLowDiff", "-price", "-turnoverK"]


#TODO: crawl failed
def getToday(): #'109/01/01'
    url = api_url.format('TAI', '-volume')
    response = requests.get(url, headers=headers)
    responseDict = json.loads(response.text)
    rankTime = responseDict['rankTime']
    ptime = datetime.strptime(rankTime, "%Y-%m-%dT%X+08:00")
    stime = datetime.strftime(ptime, "%Y/%m/%d")
    stime = stime.replace(stime[:4], str(int(stime[:4]) - 1911))
    return stime

def rank100(tType, tseORotc, isTest=False):
    if(isTest):
        request = ''
        with open('./test/test-file.html', 'r', encoding='utf-8') as f:
            request = f.read()
        return str(BeautifulSoup(request, 'lxml').select('table')[2])
    request = requests.get(url.format(tType, tseORotc), headers=headers)
    request.encoding = 'Big5-hkscs'
    print('status:', request.status_code)
    print(len(request.text))
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

def getAPI(t, s):
    url = api_url.format(t, s)
    return requests.get(url).text

def get(tseORotc):
    allContent = ''
    todayHTML = f'{todayPath}/{tseORotc}.html'

    #get all table
    #for t, c in zip(tType, chType[tseORotc]):
    #    allContent = allContent + '<div>' + rank100(t, tseORotc) + '</div>\n<hr>'
    #    print(f'[DEBUG]{c}')
        
    #get all table
    for t in api_tt:
        for e,s in enumerate(api_sort):
            allContent = allContent + '<div>' + getAPI(t, s) + '</div>\n<hr>'
            print(f'[DEBUG]{chType[t][e]}')

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

def copyDirToArchives(targetDir):
    srcPath = f'./src/{targetDir}/'
    dstPath = f'./archives/{targetDir}/'
    copytree(srcPath, dstPath)
    print(f'[DEBUG]copy tail dir {srcPath} to archives dir')

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

    if(str(tail) != 'None'):
        #copy tail dir to archives dir
        copyDirToArchives(tail)
        #remove file(day dir)
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

def renewStatusJson(arcDay):
    dDayList = [today, "src"]
    
    with open("./status.json", 'r') as file:
        jf = json.load(file)
        dayList  = [i[0] for i in jf['raw']]
        ixe = dayList.index(arcDay)

    with open("./status.json", 'w') as file:
        jf['raw'].append(dDayList)
        jf['raw'][ixe][1] = 'archives'
        file.write(json.dumps(jf, sort_keys=True, indent=4))

    print('[DEBUG]renew status.json')

def renewSrcIndexAndSubdir(today):
    srcIndex = './src/index.html'
    soup = BeautifulSoup(loadFile(srcIndex), 'lxml')
    d0Tag = soup.select('#d0')[0]

    #avoid duplicate renew
    if(d0Tag.string == today):
        print(f'[DEBUG]avoid duplicate renew {srcIndex}')
        return

    removeTailFileAndDir(soup)
    renewStatusJson(soup.select('#d9')[0].string)
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
