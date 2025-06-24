import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
import base64
from typing import List, Dict, Any, Tuple, Optional

def create_bar_chart(data: List[Dict[str, Any]], x_key: str, y_key: str, title: str, xlabel: str, ylabel: str) -> str:
    """
    创建柱状图并返回base64编码的图像
    
    参数:
    - data: 数据列表
    - x_key: X轴数据的键名
    - y_key: Y轴数据的键名
    - title: 图表标题
    - xlabel: X轴标签
    - ylabel: Y轴标签
    
    返回:
    - base64编码的图像
    """
    plt.figure(figsize=(10, 6))
    df = pd.DataFrame(data)
    
    # 绘制柱状图
    sns.barplot(x=x_key, y=y_key, data=df)
    
    # 设置标题和标签
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 将图像转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return image_base64

def create_line_chart(data: List[Dict[str, Any]], x_key: str, y_key: str, title: str, xlabel: str, ylabel: str) -> str:
    """
    创建折线图并返回base64编码的图像
    
    参数与create_bar_chart相同
    """
    plt.figure(figsize=(10, 6))
    df = pd.DataFrame(data)
    
    # 绘制折线图
    sns.lineplot(x=x_key, y=y_key, data=df)
    
    # 设置标题和标签
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 将图像转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return image_base64

def create_heatmap(data: pd.DataFrame, title: str) -> str:
    """
    创建热力图并返回base64编码的图像
    
    参数:
    - data: 包含相关性数据的DataFrame
    - title: 图表标题
    
    返回:
    - base64编码的图像
    """
    plt.figure(figsize=(10, 8))
    
    # 绘制热力图
    sns.heatmap(data, annot=True, cmap='coolwarm', linewidths=0.5)
    
    # 设置标题
    plt.title(title)
    plt.tight_layout()
    
    # 将图像转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return image_base64

def create_pie_chart(data: List[Dict[str, Any]], value_key: str, label_key: str, title: str) -> str:
    """
    创建饼图并返回base64编码的图像
    
    参数:
    - data: 数据列表
    - value_key: 数值的键名
    - label_key: 标签的键名
    - title: 图表标题
    
    返回:
    - base64编码的图像
    """
    plt.figure(figsize=(10, 10))
    df = pd.DataFrame(data)
    
    # 绘制饼图
    plt.pie(df[value_key], labels=df[label_key], autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # 使饼图为正圆形
    
    # 设置标题
    plt.title(title)
    plt.tight_layout()
    
    # 将图像转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return image_base64

def create_scatter_plot(data: List[Dict[str, Any]], x_key: str, y_key: str, title: str, xlabel: str, ylabel: str, 
                        hue_key: Optional[str] = None) -> str:
    """
    创建散点图并返回base64编码的图像
    
    参数:
    - data: 数据列表
    - x_key: X轴数据的键名
    - y_key: Y轴数据的键名
    - title: 图表标题
    - xlabel: X轴标签
    - ylabel: Y轴标签
    - hue_key: 用于分组的键名（可选）
    
    返回:
    - base64编码的图像
    """
    plt.figure(figsize=(10, 6))
    df = pd.DataFrame(data)
    
    # 绘制散点图
    if hue_key and hue_key in df.columns:
        sns.scatterplot(x=x_key, y=y_key, hue=hue_key, data=df)
        plt.legend(title=hue_key)
    else:
        sns.scatterplot(x=x_key, y=y_key, data=df)
    
    # 设置标题和标签
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    
    # 将图像转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return image_base64
