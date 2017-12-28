import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from urllib.parse import parse_qs
from time import strftime
from time import localtime

LOGIN_INFO = {
    'user_id': 'ID',
    'password': 'PASSWORD'
}
URL = 'https://member.inven.co.kr'
ATTENDANCE_URL = 'http://imart.inven.co.kr/attendance'

with requests.Session() as s:
    # get stoken
    login_page = s.get(URL + '/user/scorpio/mlogin')
    soup = bs(login_page.text, 'html.parser')
    stoken = soup.find(id='stoken')['value']
    wsip = soup.find(id='wsip')['data-json']

    data = {**LOGIN_INFO, **{'st': stoken, 'wsip': wsip, 'kp': 0}}
    print(data)
    # login
    login_msg = s.post(URL + '/m/login/dispatch', data=data).json()
    print(login_msg)
    if 'result' in login_msg:
        if login_msg['result'] == 'security_notify':
            extend_pw = s.post(URL + '/user/scorpio/res/extend/pw', data={'mid': LOGIN_INFO['user_id']}).json()
            print(extend_pw)
            login_msg = s.post(URL + '/m/login/dispatch', data=data).json()
    elif 'error' in login_msg:
        exit()

    point = s.post(URL + '/user/scorpio/chk/skill/point').json()
    print(point)

    # attendance
    data = {'attendCode': strftime('%Y%m', localtime())}
    print(data)
    headers = {
        'Host':	'imart.inven.co.kr',
        'Referer': ATTENDANCE_URL+'/'
    }
    attend = s.post(ATTENDANCE_URL + '/attend_apply.ajax.php', headers=headers, data=data).text
    print(attend)

    # VOTE
    # get vote_page url
    attend_page = s.get(ATTENDANCE_URL + '/')
    soup = bs(attend_page.text, 'html.parser')
    vote_url = soup.select_one('.voteBttn a')['href']
    vote_page = s.get(vote_url)
    soup = bs(vote_page.text, 'html.parser')
    iframes = soup.select('iframe')
    for iframe in iframes:
        if iframe['src'].find('vidx') > -1:
            # get vidx
            print(iframe['src'])
            url = urlparse(iframe['src'])
            vidx = parse_qs(url.query)['vidx'][0]
            data = {'vidx': vidx, 'rurl': 'close', 'answer[]': 1, 'content': ''}
            # vote
            vote = s.post('http://www.inven.co.kr/common/invenvote/vote_entry.php', data=data)
            print(vote.text.strip())
