import pandas as pd
import numpy as np
import random

def get_max_decimal_places(column):
    """计算一列数据中最长的小数位数（处理浮点数精度问题）"""
    max_decimals = 0
    for value in column:
        if pd.isna(value):
            continue
        
        # 处理浮点数精度问题，先四舍五入到合理位数
        rounded_val = round(float(value), 10)
        str_val = str(rounded_val)
        
        if '.' in str_val:
            # 分割后去除末尾0，计算有效小数位
            decimal_part = str_val.split('.')[1].rstrip('0')
            decimals = len(decimal_part) if decimal_part else 0
            if decimals > max_decimals:
                max_decimals = decimals
    return max_decimals

def process_data(data, method):
    valid_methods = {'mean', 'median', 'mode', 'ffill', 'bfill', 'interpolate'}
    
    if method not in valid_methods:
        raise ValueError(f"无效的方法: {method}，必须是以下之一: {valid_methods}")
    
    # 检查每列数据类型
    str_columns = {}  # 存储纯字符串列
    num_columns = {}  # 存储纯数字列
    
    for key, values in data.items():
        has_str = False
        has_num = False
        
        for val in values:
            if val is None:  # 忽略null值
                continue
            if isinstance(val, str):
                has_str = True
            elif isinstance(val, (int, float)):
                has_num = True
        
        # 同时存在字符串和数字，抛出错误
        if has_str and has_num:
            raise ValueError(f"列 '{key}' 同时包含字符串和数字类型，无法处理")
        
        if has_str:
            str_columns[key] = values
        else:
            num_columns[key] = values
    
    # 处理数字列：对齐长度
    aligned_num_data = {}
    if num_columns:
        max_length = max(len(values) for values in num_columns.values())
        for key, values in num_columns.items():
            if len(values) < max_length:
                aligned_values = values + [0] * (max_length - len(values))
            else:
                aligned_values = values[:max_length]
            aligned_num_data[key] = aligned_values
        
        # 转换为DataFrame处理原始缺失值（None）
        df = pd.DataFrame(aligned_num_data)
        df.replace([None], np.nan, inplace=True)
        filled_df = df.copy()
        
        # 按指定方法填充缺失值（修改部分：移除inplace=True，改为直接赋值）
        if method == 'mean':
            for col in filled_df.columns:
                mean_val = filled_df[col].mean()
                # 改为直接赋值，避免inplace=True在副本上操作
                filled_df[col] = filled_df[col].fillna(mean_val if not np.isnan(mean_val) else 0)
        
        elif method == 'median':
            for col in filled_df.columns:
                median_val = filled_df[col].median()
                # 核心修改：移除inplace=True，使用赋值方式
                filled_df[col] = filled_df[col].fillna(median_val if not np.isnan(median_val) else 0)
        
        elif method == 'mode':
            for col in filled_df.columns:
                non_na_values = filled_df[col].dropna()
                if non_na_values.empty:
                    fill_val = 0
                else:
                    value_counts = non_na_values.value_counts()
                    if len(value_counts) > 0 and value_counts.iloc[0] > 1:
                        fill_val = value_counts.index[0]
                    else:
                        fill_val = random.choice(non_na_values.tolist())
                # 同样改为赋值方式
                filled_df[col] = filled_df[col].fillna(fill_val)
        
        elif method == 'ffill':
            # 对于整表操作，保持inplace=True是安全的
            filled_df.ffill(inplace=True)
            filled_df.bfill(inplace=True)
        
        elif method == 'bfill':
            filled_df.bfill(inplace=True)
            filled_df.ffill(inplace=True)
        
        elif method == 'interpolate':
            filled_df.bfill(limit=1, inplace=True)
            filled_df.interpolate(method='linear', inplace=True)
            filled_df.ffill(inplace=True)
        
        # 所有数字保留两位小数
        num_result = {}
        format_str = ".2f"
        for col in filled_df.columns:
            col_values = filled_df[col].astype(float).round(2)
            formatted_values = [float(f"{x:{format_str}}") for x in col_values]
            num_result[col] = formatted_values
    else:
        num_result = {}
    
    # 合并字符串列和处理后的数字列，保持原始顺序
    result = {}
    for key in data.keys():
        if key in str_columns:
            result[key] = str_columns[key]
        else:
            result[key] = num_result[key]
    
    return result
