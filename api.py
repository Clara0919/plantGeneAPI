from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import getData
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs



app = Flask(__name__)
@app.route('/api/getData', methods=['GET'])
def get_data():
    # 用於傳入基因位置 request.args.get('position') 
    position= 'Chr1:1,489,366..1,499,365'
    # 暫時用於傳入sessionId request.args.get('position') 
    sessionId='302EEB1F6096906C540B6C36553A1134'
    data, status_code = getData.getGeneData(position,sessionId)
    
    if status_code==200:
        context=data
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
            area_data.append(name)
        return jsonify({"status": "成功", "data": area_data}), 200

            
        
    else:   
        return jsonify({"status": "失敗", "data": data}), status_code

@app.route('/api/getId', methods=['GET'])
def get_id():
    position = request.args.get('position')
    sessionId=request.args.get('sessionId')
    data, status_code = getData.getLocusId(position,sessionId)
    if status_code==200:
        return data
    else:
        return '取得 locus id 失敗'

if __name__ == '__main__':
    app.run(debug=True)
