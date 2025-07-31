# 数据处理API服务运行指南

## 项目介绍
这是一个基于Flask开发的数据处理API服务，专注于提供高效的缺失值填充功能。该服务支持六种常用填充方法，包括均值填充、中位数填充、众数填充、前向填充、后向填充和线性插值填充，可通过API接口便捷地处理包含缺失值的数据。

## 运行步骤

### 1. 环境准备与依赖安装
- 确保已安装Python 3.6及以上版本
- 安装项目所需依赖包：
```bash
pip install -r requirements.txt
```
依赖说明：
- Flask==2.2.3：用于搭建Web服务
- pandas==1.3.3：用于数据处理
- numpy==1.21.2：用于数值计算

### 2. 启动Flask应用
在项目根目录（如`d:\coding\python\python南威\机器学习算法`）下执行以下命令：
```bash
python app.py
```
启动成功后，将看到类似以下输出：
```
* Serving Flask app 'app' (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: on
* Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 123-456-789
```

### 3. API接口使用说明
服务提供`/fill_missing_values`接口用于处理缺失值，支持POST方法调用。

#### 请求参数说明
- 必须包含`data`字段：字典类型，键为列名，值为包含缺失值（用`null`表示）的数组
- 必须包含`method`字段：字符串类型，指定填充方法，可选值如下：
  - `mean`：均值填充
  - `median`：中位数填充
  - `mode`：众数填充
  - `ffill`：前向填充
  - `bfill`：后向填充
  - `interpolate`：线性插值填充

#### 调用示例
1. 使用curl调用：
```bash
curl -X POST http://localhost:5000/fill_missing_values \
  -H "Content-Type: application/json" \
  -d '{"data":{"col1":[1,4,7],"col2":[2,null,8],"col3":[null,6,9]},"method":"mean"}'
```

2. 请求体示例：
```json
{
  "data": {
    "col1": [1, 4, 7],
    "col2": [2, null, 8],
    "col3": [null, 6, 9]
  },
  "method": "mean"
}
```

#### 响应说明
- 成功响应：返回填充后的结果数据，格式为`{"result": {列名: [填充后的值数组]}}`
- 错误响应：返回错误信息，格式为`{"error": "错误类型", "message": "错误详情"}`

### 4. 项目结构
```
机器学习算法/
├── README.md                  # 项目说明文档
├── app.py                     # Flask应用入口，定义API接口
├── requirements.txt           # 项目依赖清单
├── test_result_field.py       # 接口测试脚本
├── filled_results.json        # 示例结果文件
└── machine_learning_alg/
    ├── data_processor.py      # 数据处理核心逻辑，实现缺失值填充算法
    └── all_imputation_methods_test.json  # 测试数据文件
```

## 功能说明
1. 数据对齐：自动以最长数据列为标准对齐所有列，短数据列将用0填充补齐
2. 缺失值处理：将`null`转换为`NaN`进行统一处理
3. 填充逻辑：
   - 均值/中位数填充：按列计算均值/中位数并填充缺失值
   - 众数填充：优先使用出现次数最多的值，无明显众数时随机选择非缺失值
   - 前向填充：使用前一个非缺失值填充，首行缺失值将用后向填充补充
   - 后向填充：使用后一个非缺失值填充，末行缺失值将用前向填充补充
   - 线性插值：通过线性插值计算缺失值，边界缺失值用前后向填充补充
4. 结果格式化：所有结果保留两位小数，确保数据格式一致性
