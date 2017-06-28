from bs4 import BeautifulSoup
import cookielib, urllib2, urllib
from time import strftime, localtime

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

ID = 'ID'
PASSWORD = 'PWD'
URL = 'https://member.inven.co.kr'

class Requestor:
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    # def __init__(self):

    def get(self, url, params, isSet):
        print url
        req = urllib2.Request(url, params)
        if (isSet):
            req.add_header('Accept', '*/*')
            req.add_header('Accept-Encoding', 'gzip, deflate')
            req.add_header('Accept-Language', 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4')
            req.add_header('Cache-Control', 'no-cache')
            req.add_header('Connection', 'keep-alive')
            req.add_header('Content-Length', '17')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            req.add_header('Host', 'imart.inven.co.kr')
            req.add_header('Origin', 'http://imart.inven.co.kr')
            req.add_header('Pragma', 'no-cache')
            req.add_header('Referer', 'http://imart.inven.co.kr/attendance/')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36')
            req.add_header('X-Requested-With', 'XMLHttpRequest')
        print req.headers
        res = opener.open(req)
        return BeautifulSoup(res.read(), 'html.parser')

req = Requestor();
stoken = req.get(URL + '/user/scorpio/mlogin', {}, False).find(id='stoken')['value']

params = urllib.urlencode({
    'st': stoken,
     'kp': 0,
     'user_id': ID,
     'password': PASSWORD
})
print req.get(URL + '/m/login/dispatch', params, False)
params = urllib.urlencode({
    'mid': ID
})
print req.get(URL + '/user-scorpio/extend_pw_result.php', params, False)
print req.get(URL + '/user/scorpio/chk/skill/point', {}, False)

attendCode = strftime('%Y%m',localtime())
params = urllib.urlencode({'attendCode': attendCode})
print req.get('http://imart.inven.co.kr/attendance/attend_apply.ajax.php', params, True)

params = urllib.urlencode({
    'vidx': 3480,
    'rurl': 'close',
    'answer[]': 24,
    'answer[]': 28,
    'content': ''
})
# req.get('http://www.inven.co.kr/common/invenvote/vote_entry.php', params, False)