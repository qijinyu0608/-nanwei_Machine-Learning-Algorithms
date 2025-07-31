# 数据处理API服务运行指南

## 项目介绍
这是一个基于Flask的数据处理API服务，提供缺失值填充功能，支持六种填充方法（均值、中位数、众数、前向填充、后向填充、线性插值）。

## 运行步骤

### 1. 安装依赖
首先，确保已安装Python 3.6+，然后安装项目所需依赖：

```bash
# 使用pip安装依赖
pip install -r requirements.txt
```

### 2. 启动Flask应用
在项目根目录下（`d:\coding\python\python南威\机器学习算法`），执行以下命令启动Flask应用：

```bash
python app.py
```

启动成功后，会看到类似以下输出：
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

### 3. 测试API接口
应用启动后，可以通过以下两种方式测试API接口：

#### 方式一：使用测试脚本
运行项目根目录下的`test_result_field.py`脚本：

```bash
python test_result_field.py
```

该脚本会测试`/process_data`和`/process_file`两个接口，并输出测试结果。

#### 方式二：使用Postman或curl

1. 测试`/process_data`接口（直接发送JSON数据）：
   - URL: `http://localhost:5000/process_data`
   - Method: `POST`
   - Headers: `Content-Type: application/json`
   - Body (示例):
     ```json
     {
       "data": [
         [1, 2, null],
         [4, null, 6],
         [7, 8, 9]
       ],
       "method_index": 1
     }
     ```

2. 测试`/process_file`接口（上传JSON文件）：
   - URL: `http://localhost:5000/process_file`
   - Method: `POST`
   - Form Data: 选择`file`字段，上传包含`data`和可选`method_index`字段的JSON文件

### 4. 查看结果
API响应会包含以下字段：
- `status`: 处理状态（`success`或`error`）
- `result`: 填充后的结果数据（当`status`为`success`时）
- `method_index`: 使用的填充方法索引
- `method`: 使用的填充方法名称
- `message`: 错误信息（当`status`为`error`时）

## 填充方法说明
- `method_index=1`: 均值填充
- `method_index=2`: 中位数填充
- `method_index=3`: 众数填充
- `method_index=4`: 前向填充
- `method_index=5`: 后向填充
- `method_index=6`: 线性插值填充

## 项目结构
```
机器学习算法/
├── README.md           # 项目说明文档
├── app.py              # Flask应用入口
├── requirements.txt    # 项目依赖
├── test_result_field.py # 测试脚本
├── filled_results.json  # 示例结果文件
└── machine_learning_alg/
    ├── data_processor.py  # 数据处理核心类
    └── all_imputation_methods_test.json  # 测试数据文件
```