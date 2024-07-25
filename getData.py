import requests

def getGeneData():
    # 取得jsessionid
    url = "https://gbrowse.arabidopsis.org/cgi-bin/gb2/gbrowse/arabidopsis/"
    session = requests.Session()
    getCookieHeaders = {
    'authority': 'www.googletagmanager.com',
    'method': 'GET',
    'path': '/gtag/js?id=G-S17ZS9ZPHD',
    'scheme': 'https',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-TW,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Dnt': '1',
    'Pragma': 'no-cache',
    'Referer': 'https://www.arabidopsis.org/',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }
    cookieResponse = session.get('https://www.arabidopsis.org/',headers=getCookieHeaders)
    jsessionid = cookieResponse.cookies.get("JSESSIONID")
    
    
    # 取得locus資料
    headers = {
    'Accept-Language': 'zh-TW,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Dnt': '1',
    'Origin': 'https://gbrowse.arabidopsis.org',
    'Pragma': 'no-cache',
    'Referer': 'https://gbrowse.arabidopsis.org/',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
    # print(jsessionid)
    cookies = {
     'JSESSIONID': 'B882D91F72680B769F9636EF658AFC3F',
}
    files = {
    'action': (None, 'retrieve_multiple'),
    'track_ids': (None, 'Locus'),
    'tk_BAC': (None, '02f81043270e01e70271c994cf26b37f'),
    'tk_Locus': (None, 'f5743086a42323467d59420b38d34f39'),
    'tk_ProteinCoding': (None, '499ac2f3b4a1c87929868c85f0d6974f'),
    'tk_Pseudogene': (None, 'b4bfbb230c370b0bb74d86956a1b6b38'),
    'tk_ncRNAs': (None, 'c01d5d87e8a42685a84df8498fd94611'),
    'tk_cDNA': (None, '8a408d8c6c2af085ea18f605bf30458b'),
    'tk_tDNAs': (None, 'a2bbb8fd84ac63670ded3f13cab62ea2'),
    'tk_Polymorphism': (None, '556af7dcdb0c44bb3af02512fa70ef0c'),
    'tk_Marker': (None, '42442feee001037d4422334e08055acf'),
}

    # 使用 requests.post 發送 POST 請求
    response = requests.post(
    'https://gbrowse.arabidopsis.org/cgi-bin/gb2/gbrowse/arabidopsis/',
    cookies=cookies,
    headers=headers,
    files=files
)
    if response.status_code == 200:
        # print(response.text)
        return response.text, response.status_code
    else:
        # print("請求失敗，狀態:", response.status_code)
        return ("請求失敗，狀態:"), response.status_code

