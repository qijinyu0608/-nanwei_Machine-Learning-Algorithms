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

def process_data(data, method):  # 修改参数为method（字符串类型）
    valid_methods = {'mean', 'median', 'mode', 'ffill', 'bfill', 'interpolate'}
    
    if method not in valid_methods:
        raise ValueError(f"无效的方法: {method}，必须是以下之一: {valid_methods}")
    
    # 以最长数据为标准对齐，短数据补0
    max_length = max(len(values) for values in data.values())
    aligned_data = {}
    for key, values in data.items():
        if len(values) < max_length:
            aligned_values = values + [0] * (max_length - len(values))
        else:
            aligned_values = values[:max_length]
        aligned_data[key] = aligned_values
    
    # 转换为DataFrame处理原始缺失值（None）
    df = pd.DataFrame(aligned_data)
    df.replace([None], np.nan, inplace=True)
    filled_df = df.copy()
    
    # 按指定方法填充缺失值
    if method == 'mean':
        for col in filled_df.columns:
            mean_val = filled_df[col].mean()
            filled_df[col].fillna(mean_val if not np.isnan(mean_val) else 0, inplace=True)
    
    elif method == 'median':
        for col in filled_df.columns:
            median_val = filled_df[col].median()
            filled_df[col].fillna(median_val if not np.isnan(median_val) else 0, inplace=True)
    
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
            filled_df[col].fillna(fill_val, inplace=True)
    
    elif method == 'ffill':
        filled_df.ffill(inplace=True)
        filled_df.bfill(inplace=True)
    
    elif method == 'bfill':
        filled_df.bfill(inplace=True)
        filled_df.ffill(inplace=True)
    
    elif method == 'interpolate':
        filled_df.bfill(limit=1, inplace=True)
        filled_df.interpolate(method='linear', inplace=True)
        filled_df.ffill(inplace=True)
    
    # 所有数据保留两位小数
    result = {}
    format_str = ".2f"  # 固定保留两位小数

    for col in filled_df.columns:
        # 确保所有数值都转为浮点数并四舍五入到两位小数
        col_values = filled_df[col].astype(float).round(2)
        # 格式化为字符串（补零），再转回float
        formatted_values = [float(f"{x:{format_str}}") for x in col_values]
        result[col] = formatted_values
    
    return result