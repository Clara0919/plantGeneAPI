import requests
import json
from flask import Flask, jsonify

headers = {
    'Accept-Language': 'zh-TW,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Dnt': '1',
    'Origin': 'https://gbrowse.arabidopsis.org',
    'Pragma': 'no-cache',
    'Referer': 'https://gbrowse.arabidopsis.org/cgi-bin/gb2/gbrowse/arabidopsis/',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}



# def getSessionId():
#     # 取得jsessionid
#     session = requests.Session()
#     getCookieHeaders = {
#     'authority': 'www.googletagmanager.com',
#     'method': 'GET',
#     'path': '/gtag/js?id=G-S17ZS9ZPHD',
#     'scheme': 'https',
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Accept-Language': 'zh-TW,zh;q=0.9',
#     'Cache-Control': 'no-cache',
#     'Dnt': '1',
#     'Pragma': 'no-cache',
#     'Referer': 'https://www.arabidopsis.org/',
#     'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#     'Sec-Ch-Ua-Mobile': '?0',
#     'Sec-Ch-Ua-Platform': '"macOS"',
#     'Sec-Fetch-Dest': 'script',
#     'Sec-Fetch-Mode': 'no-cors',
#     'Sec-Fetch-Site': 'cross-site',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
#     }
#     cookieResponse = session.get('https://www.arabidopsis.org/',headers=getCookieHeaders)
#     jsessionid = cookieResponse.cookies.get("JSESSIONID")
#     # print(jsessionid)
#     return jsessionid

def getLocusId(position,sessionId):
    # 取得locus資料
    files = {
    'action': (None, 'navigate'),
    'navigate': (None, 'left 0'),
    'view_start': (None, 'NaN'),
    'view_stop': (None, 'NaN'),
    'snapshot': (None, 'false'),
}
    params = {
    'name': position,
}
    cookies = {
    'JSESSIONID': sessionId,
}
    
    # 使用 requests.post 發送 POST 請求
    response = requests.post(
    'https://gbrowse.arabidopsis.org/cgi-bin/gb2/gbrowse/arabidopsis/',
    cookies=cookies,
    params=params,
    headers=headers,
    files=files
)  
    if response.status_code==200:
    # 解析 JSON 資料
        parsed_data = json.loads(response.text)
    # 提取 locus 的值
        locus_id = parsed_data["track_keys"]["Locus"]
        return locus_id, response.status_code
    else:
        return ("無法取得locusId", response.status_code)

def getGeneData(position,sessionId):
    
    url = "https://gbrowse.arabidopsis.org/cgi-bin/gb2/gbrowse/arabidopsis/"
    
    locusId=getLocusId(position,sessionId)

    files = {
    'action': (None, 'retrieve_multiple'),
    'track_ids': (None, 'Locus'),
    'tk_Locus': (None, locusId),
}
    
    cookies = {
    'JSESSIONID': sessionId,
}

    # 使用 requests.post 發送 POST 請求
    response = requests.post(
    url,
    cookies=cookies,
    headers=headers,
    files=files
)
    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return ("請求失敗，狀態:"), response.status_code
    


