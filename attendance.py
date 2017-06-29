import cookielib
import urllib2
import urllib
import json
from time import strftime, localtime
from bs4 import BeautifulSoup

ID = 'ID'
PASSWORD = 'PASSWORD'
URL = 'https://member.inven.co.kr'


class Request:
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def get_plain(self, url, params='', headers={}):
        print url
        request = urllib2.Request(url, params, headers)
        print request.headers
        response = self.opener.open(request)
        return response.read()

    def get_bs(self, url, params='', headers={}):
        response = self.get_plain(url, params, headers)
        return BeautifulSoup(response, 'html.parser')

    def get_json(self, url, params='', headers={}):
        response = self.get_plain(url, params, headers)
        return json.loads(response)

req = Request()
STOKEN = req.get_bs(URL + '/user/scorpio/mlogin').find(id='stoken')['value']

params = urllib.urlencode({
    'st': STOKEN,
    'kp': 0,
    'user_id': ID,
    'password': PASSWORD
})
print req.get_json(URL + '/m/login/dispatch', params)
params = urllib.urlencode({
    'mid': ID
})
print req.get_json(URL + '/user-scorpio/extend_pw_result.php', params)
print req.get_json(URL + '/user/scorpio/chk/skill/point')

# TODO login error
attendCode = strftime('%Y%m', localtime())
params = urllib.urlencode({'attendCode': attendCode})
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '17',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'imart.inven.co.kr',
    'Origin': 'http://imart.inven.co.kr',
    'Pragma': 'no-cache',
    'Referer': 'http://imart.inven.co.kr/attendance/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
print req.get_plain('http://imart.inven.co.kr/attendance/attend_apply.ajax.php', params, headers)

# TODO GET vidx
# VOTE_URL = req.get_bs('http://imart.inven.co.kr/attendance/').find(class_='voteBttn').contents[1]['href']
# print 'VOTE_URL: ' + VOTE_URL
# print req.get_bs(VOTE_URL).find_all('iframe', name='vidx')
# # print 'VIDX: ' + VIDX
# params = urllib.urlencode({
#     'vidx': 3504,
#     'rurl': 'close',
#     'answer[]': 24,
#     'answer[]': 28,
#     'content': ''
# })
# print req.get('http://www.inven.co.kr/common/invenvote/vote_entry.php', params, False)
