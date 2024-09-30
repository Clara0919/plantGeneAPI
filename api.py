from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import getData
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from flask_cors import CORS  # 引入 CORS
app = Flask(__name__)
CORS(app)  # 設置全局 CORS

@app.route('/api/getId', methods=['GET'])
def get_id():
    position = request.args.get('position')
    sessionId=request.args.get('sessionId')
    data, status_code= getData.getLocusId(position,sessionId)
    data_dict = json.loads(data)

    if status_code==200:
        context=data_dict['track_html']['Locus']
        # 提取所有 <area> 標籤中的資料
        area_data = []
        soup = BeautifulSoup(context, "html.parser") 
  
        areas = soup.find_all('area')
        for area in areas:
            href = area.get('href')
            cleanHref=href.replace('\\\"', '')
            parsed_url = urlparse(cleanHref)
            query_params = parse_qs(parsed_url.query)
            name = query_params.get("name", [None])[0]
            mouseoverText=area.get('onmouseover')
   
            chrStart,chrEnd =getData.getRange(mouseoverText)
            positionStart,positionEnd=getData.getRange(position)
            rangeMatch=getData.rangeOverlap(positionStart,positionEnd,chrStart,chrEnd)
            if rangeMatch:
             area_data.append(name)
        
        # 將 area_data 轉換為逗號分隔的字串
        area_data_string = ','.join(area_data)
        return jsonify({"status": "成功", "data": area_data_string}), 200
    else:
        return jsonify({"errormsg": '取得 locus id 失敗'})

if __name__ == '__main__':
    app.run()
