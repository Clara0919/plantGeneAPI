import requests
import json
import re
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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Prototype-Version': '1.7',
        'X-Requested-With': 'XMLHttpRequest',
}
url = 'https://gbrowse.arabidopsis.org/cgi-bin/gb2/gbrowse/arabidopsis/'

cookies = {
    'JSESSIONID': '',
}

def renewWebsite(params):
    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        params=params,  # 如果你在 URL 中需要參數
    )
    return response
# 取得locusId 
def getLocusId(position,sessionId):

    global cookies
    cookies['JSESSIONID'] = sessionId
    data = {
        'action': 'navigate',
        'navigate': 'left 0',
        'view_start': 'NaN',
        'view_stop': 'NaN',
        'snapshot': 'false'
    }
    params = {
    'name': position,
    }
    # 取得位置id前需要先呼叫刷新頁面來更新對話,否則會取到錯誤資料
    renewWebsite(params)

    # 使用 requests.post 發送 POST 請求
    response = requests.post(
        url,
        headers=headers,
        cookies=cookies,
        params=params,  # 如果你在 URL 中需要參數
        data=data  # 使用 data 來提交表單數據
    )
    if response.status_code==200:
    # 解析 JSON 資料
        parsed_data = json.loads(response.text)
    # 提取 locusId
        locus_id = parsed_data["track_keys"]["Locus"]
        # 透過locusId取得基因名稱
        return getGeneData(locus_id) 
    else:
        return ("無法取得locusId", response.status_code)

def getGeneData(locusId):
    data = {
    'action': 'retrieve_multiple',
    'track_ids': 'Locus',
    'tk_Locus': locusId,
    }

    # 使用 requests.post 發送 POST 請求
    response = requests.post(
    url,
    cookies=cookies,
    headers=headers,
    data=data
    )
    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return ("請求失敗，狀態:"), response.status_code
    
def getRange(str):
    print("str",str)
    match = re.search(r'Chr\d+:(\d+)\.\.(\d+)',str)
    if match:
            start = match.group(1)
            end = match.group(2)
            return start, end
    else:
            print("未找到數字範圍")
    
def rangeOverlap(start_a, end_a, start_b, end_b):
    #檢查是否重疊
    return start_a <= end_b and start_b <= end_a



