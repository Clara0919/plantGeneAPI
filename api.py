from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import getData
from bs4 import BeautifulSoup



app = Flask(__name__)
@app.route('/api/getData', methods=['GET'])
def get_data():
    data, status_code = getData.getGeneData()
    
    if status_code==200:
        context=data
        # 提取所有 <area> 標籤中的資料
        area_data = []
        soup = BeautifulSoup(context, "html.parser") 
  
        areas = soup.find_all('area')
        
        for area in areas:
            href = area.get('href')
            area_data.append({'href': href.replace('\\\"', '')})
        return jsonify({"status": "成功", "data": area_data}), 200

            
        
    else:   
        return jsonify({"status": "失敗", "data": data}), status_code

  
            

if __name__ == '__main__':
    app.run(debug=True)
