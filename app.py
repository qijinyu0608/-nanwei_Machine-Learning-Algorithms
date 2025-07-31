from flask import Flask, request, make_response, jsonify
import json
from machine_learning_alg.data_processor import process_data

app = Flask(__name__)

@app.route('/fill_missing_values', methods=['POST'])
def fill_missing_values():
    try:
        # 获取请求 JSON 数据
        request_data = request.get_json()
        
        # 校验必要字段
        if not all(key in request_data for key in ['data', 'method']):
            return jsonify_error("输入格式不正确", "必须包含 'data' 和 'method' 字段"), 400
        
        # 提取参数
        data = request_data['data']
        method = request_data['method']
        
        # 校验 method 类型为字符串
        if not isinstance(method, str):
            return jsonify_error("参数类型错误", "method 必须是字符串"), 400
        
        # 处理数据
        result = process_data(data, method)
        
        # 紧凑生成 JSON：无缩进、去掉空格
        compact_json = json.dumps(
            {"result": result}, 
            indent=None,  # 无缩进
            separators=(',', ':')  # 去掉键值对之间的空格
        )
        
        # 构造响应（确保内容为纯文本 JSON，无额外格式化）
        response = make_response(compact_json)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    except ValueError as ve:
        return jsonify_error("处理错误", str(ve)), 400
    except Exception as e:
        return jsonify_error("服务器错误", str(e)), 500

def jsonify_error(error_type, message):
    """统一错误响应格式"""
    return make_response(
        json.dumps({"error": error_type, "message": message}, indent=None, separators=(',', ':'))
    )

if __name__ == '__main__':
    app.run(debug=True)