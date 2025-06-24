import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta

def group_by_time_window(data: List[Dict[str, Any]], time_key: str, window_size: str = '1H'):
    """
    按时间窗口对数据分组
    
    参数:
    - data: 数据列表，每个元素是一个字典
    - time_key: 时间字段的键名
    - window_size: 时间窗口大小，如'1H'表示1小时，'15min'表示15分钟
    
    返回:
    - 分组后的数据
    """
    df = pd.DataFrame(data)
    df[time_key] = pd.to_datetime(df[time_key])
    df['time_window'] = df[time_key].dt.floor(window_size)
    
    return df.groupby('time_window').agg(list).reset_index().to_dict(orient='records')

def calculate_statistics(data: List[Dict[str, Any]], value_key: str):
    """
    计算数据统计信息
    
    参数:
    - data: 数据列表，每个元素是一个字典
    - value_key: 要计算统计信息的键名
    
    返回:
    - 统计信息字典
    """
    values = [item[value_key] for item in data if value_key in item]
    
    if not values:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
            "std": None
        }
    
    return {
        "count": len(values),
        "mean": np.mean(values),
        "median": np.median(values),
        "min": np.min(values),
        "max": np.max(values),
        "std": np.std(values) if len(values) > 1 else 0
    }

def find_correlation(data: List[Dict[str, Any]], x_key: str, y_key: str):
    """
    计算两个变量之间的相关性
    
    参数:
    - data: 数据列表，每个元素是一个字典
    - x_key: 第一个变量的键名
    - y_key: 第二个变量的键名
    
    返回:
    - 相关系数
    """
    df = pd.DataFrame(data)
    if x_key not in df.columns or y_key not in df.columns:
        return None
    
    return df[x_key].corr(df[y_key])

def detect_anomalies(data: List[Dict[str, Any]], value_key: str, threshold: float = 2.0):
    """
    检测异常值
    
    参数:
    - data: 数据列表，每个元素是一个字典
    - value_key: 要检测的值的键名
    - threshold: Z分数阈值，超过该值视为异常
    
    返回:
    - 异常数据列表
    """
    df = pd.DataFrame(data)
    if value_key not in df.columns:
        return []
    
    mean = df[value_key].mean()
    std = df[value_key].std()
    
    if std == 0:
        return []
    
    df['z_score'] = (df[value_key] - mean) / std
    anomalies = df[abs(df['z_score']) > threshold].to_dict(orient='records')
    
    return anomalies
