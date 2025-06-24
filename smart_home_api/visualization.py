import traceback
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import argparse

# 设置可视化图表保存目录
# 在脚本所在目录下创建visualizations文件夹
VISUALIZATION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visualizations")

# 确保目录存在
if not os.path.exists(VISUALIZATION_DIR):
    os.makedirs(VISUALIZATION_DIR)
    print(f"创建可视化图表目录: {VISUALIZATION_DIR}")
else:
    print(f"使用现有可视化图表目录: {VISUALIZATION_DIR}")

# 设置中文字体，以正确显示中文
try:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
except:
    pass  # 如果没有对应字体，使用默认字体

# 加载环境变量
load_dotenv()

# API基础URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

def fetch_data_from_api(endpoint):
    """从API获取数据"""
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}: {response.status_code}")
        return None

def visualize_device_usage_frequency():
    """可视化设备使用频率"""
    data = fetch_data_from_api("analytics/device-usage-frequency")
    if not data:
        return
    
    # 转换为DataFrame
    df = pd.DataFrame(data)
    
    # 创建图表
    plt.figure(figsize=(12, 6))
    sns.barplot(x='device_name', y='usage_count', data=df)
    plt.title('设备使用频率分析')
    plt.xlabel('设备名称')
    plt.ylabel('使用次数')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 使用新路径保存图表
    output_path = os.path.join(VISUALIZATION_DIR, 'device_usage_frequency.png')
    plt.savefig(output_path)
    plt.close()
    print(f"已保存设备使用频率图表到 {output_path}")
    
    # 使用时长图表
    plt.figure(figsize=(12, 6))
    sns.barplot(x='device_name', y='total_hours', data=df)
    plt.title('设备使用总时长')
    plt.xlabel('设备名称')
    plt.ylabel('使用时长(小时)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 使用新路径保存图表
    output_path = os.path.join(VISUALIZATION_DIR, 'device_usage_duration.png')
    plt.savefig(output_path)
    plt.close()
    print(f"已保存设备使用时长图表到 {output_path}")

def visualize_device_usage_timeframe():
    """可视化设备使用时间段分布"""
    data = fetch_data_from_api("analytics/device-usage-timeframe")
    if not data:
        return
    
    # 转换为DataFrame
    df = pd.DataFrame(data)
    
    # 创建热力图
    pivot_data = df.pivot_table(index='device_name', columns='hour_of_day', values='usage_count', fill_value=0)
    
    plt.figure(figsize=(15, 10))
    sns.heatmap(pivot_data, annot=True, cmap='YlGnBu', fmt='g')
    plt.title('设备使用时间段分布')
    plt.xlabel('一天中的小时')
    plt.ylabel('设备名称')
    plt.tight_layout()
    
    # 使用新路径保存图表
    output_path = os.path.join(VISUALIZATION_DIR, 'device_usage_timeframe.png')
    plt.savefig(output_path)
    plt.close()
    print(f"已保存设备使用时间段分布图表到 {output_path}")
    
    # 为每个设备创建单独的时间段分布图
    device_names = df['device_name'].unique()
    for device in device_names:
        device_data = df[df['device_name'] == device]
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='hour_of_day', y='usage_count', data=device_data)
        plt.title(f'{device} 使用时间段分布')
        plt.xlabel('一天中的小时')
        plt.ylabel('使用次数')
        plt.xticks(range(0, 24))
        plt.tight_layout()
        
        # 使用新路径保存图表
        filename = f'device_usage_timeframe_{device.replace(" ", "_")}.png'
        output_path = os.path.join(VISUALIZATION_DIR, filename)
        plt.savefig(output_path)
        plt.close()
        print(f"已保存 {device} 使用时间段分布图表到 {output_path}")

def visualize_device_usage_patterns():
    """可视化设备使用模式（同时使用的设备）"""
    data = fetch_data_from_api("analytics/device-usage-patterns")
    if not data:
        return
    
    # 检查是否有关联规则
    if "rules" not in data or not data["rules"]:
        print("没有足够的数据来分析设备使用模式")
        return
    
    # 转换为DataFrame
    rules_df = pd.DataFrame(data["rules"])
    
    # 选择前15条规则
    top_rules = rules_df.sort_values('confidence', ascending=False).head(15)
    
    # 创建图表
    plt.figure(figsize=(12, 10))
    sns.scatterplot(
        x='support', 
        y='confidence', 
        size='lift', 
        hue='lift',
        palette='viridis',
        data=top_rules
    )
    
    # 在每个点旁边添加规则文本
    for i, row in top_rules.iterrows():
        plt.annotate(
            f"{row['antecedents']} → {row['consequents']}",
            (row['support'], row['confidence']),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=8
        )
    
    plt.title('设备使用关联规则')
    plt.xlabel('支持度')
    plt.ylabel('置信度')
    plt.tight_layout()
    
    # 使用新路径保存图表
    output_path = os.path.join(VISUALIZATION_DIR, 'device_usage_patterns.png')
    plt.savefig(output_path)
    plt.close()
    print(f"已保存设备使用模式图表到 {output_path}")

def visualize_home_area_impact():
    """可视化房屋面积对设备使用行为的影响"""
    data = fetch_data_from_api("analytics/home-area-impact")
    if not data:
        return
    
    # 转换为DataFrame
    df = pd.DataFrame(data)
    
    # 检查实际的列名并打印出来
    print("数据中的实际列名:", df.columns.tolist())
    
    # 根据实际数据结构进行可视化
    # 如果没有avg_usage_count，可能是使用usage_count
    usage_count_field = 'avg_usage_count' if 'avg_usage_count' in df.columns else 'usage_count'
    usage_hours_field = 'avg_usage_hours' if 'avg_usage_hours' in df.columns else 'total_hours'
    
    # 检查是否有必要的列
    if 'square_meters' not in df.columns:
        print("错误: 数据中缺少 'square_meters' 列")
        return
    
    if usage_count_field not in df.columns:
        print(f"错误: 数据中缺少使用次数相关列 (尝试查找 'avg_usage_count' 或 'usage_count')")
        return
    
    # 散点图：房屋面积与设备使用次数
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='square_meters', y=usage_count_field, hue='category_name', data=df)
    plt.title('房屋面积与设备使用次数的关系')
    plt.xlabel('房屋面积（平方米）')
    plt.ylabel('使用次数')
    plt.tight_layout()
    
    # 使用新路径保存图表
    output_path = os.path.join(VISUALIZATION_DIR, 'home_area_impact_count.png')
    plt.savefig(output_path)
    plt.close()
    print(f"已保存房屋面积与使用次数关系图表到 {output_path}")
    
    # 检查是否有时长数据
    if usage_hours_field in df.columns:
        # 散点图：房屋面积与设备使用时长
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='square_meters', y=usage_hours_field, hue='category_name', data=df)
        plt.title('房屋面积与设备使用时长的关系')
        plt.xlabel('房屋面积（平方米）')
        plt.ylabel('使用时长（小时）')
        plt.tight_layout()
        
        # 使用新路径保存图表
        output_path = os.path.join(VISUALIZATION_DIR, 'home_area_impact_hours.png')
        plt.savefig(output_path)
        plt.close()
        print(f"已保存房屋面积与使用时长关系图表到 {output_path}")
    
    # 检查是否能为每个类别创建回归图
    if 'category_name' in df.columns:
        categories = df['category_name'].unique()
        for category in categories:
            cat_data = df[df['category_name'] == category]
            
            # 使用次数回归图
            plt.figure(figsize=(8, 6))
            sns.regplot(x='square_meters', y=usage_count_field, data=cat_data)
            plt.title(f'{category} - 房屋面积与使用次数关系')
            plt.xlabel('房屋面积（平方米）')
            plt.ylabel('使用次数')
            plt.tight_layout()
            
            # 使用新路径保存图表
            filename = f'home_area_impact_count_{category.replace(" ", "_")}.png'
            output_path = os.path.join(VISUALIZATION_DIR, filename)
            plt.savefig(output_path)
            plt.close()
            
            # 使用时长回归图
            if usage_hours_field in df.columns:
                plt.figure(figsize=(8, 6))
                sns.regplot(x='square_meters', y=usage_hours_field, data=cat_data)
                plt.title(f'{category} - 房屋面积与使用时长关系')
                plt.xlabel('房屋面积（平方米）')
                plt.ylabel('使用时长（小时）')
                plt.tight_layout()
                
                # 使用新路径保存图表
                filename = f'home_area_impact_hours_{category.replace(" ", "_")}.png'
                output_path = os.path.join(VISUALIZATION_DIR, filename)
                plt.savefig(output_path)
                plt.close()
            
        print(f"已保存每个设备类别的房屋面积影响图表到 {output_path}")

def visualize_security_events():
    """可视化安防事件统计"""
    try:
        data = fetch_data_from_api("analytics/security-events-summary")
        if not data:
            print("警告: 无法获取安防事件数据，跳过此可视化")
            return
        
        print(f"安防事件数据类型: {type(data)}")
        
        # 处理当前返回的数据格式
        if isinstance(data, list):
            df_events = pd.DataFrame(data)
            print(f"安防事件数据列: {df_events.columns.tolist()}")
            
            # 可视化按住宅统计的事件数量
            if 'home_name' in df_events.columns and 'total_events' in df_events.columns:
                plt.figure(figsize=(12, 6))
                # 按总事件数排序
                df_sorted = df_events.sort_values('total_events', ascending=False)
                sns.barplot(x='home_name', y='total_events', data=df_sorted)
                plt.title('各住宅安防事件总数')
                plt.xlabel('住宅名称')
                plt.ylabel('事件数量')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                output_path = os.path.join(VISUALIZATION_DIR, 'security_events_by_home.png')
                plt.savefig(output_path)
                plt.close()
                print(f"已保存各住宅安防事件图表到 {output_path}")
            
            # 可视化各严重程度事件分布
            if all(col in df_events.columns for col in ['high_severity_events', 'medium_severity_events', 'low_severity_events']):
                # 计算总体严重程度分布
                severity_data = {
                    'severity': ['high', 'medium', 'low'],
                    'count': [
                        df_events['high_severity_events'].sum(),
                        df_events['medium_severity_events'].sum(),
                        df_events['low_severity_events'].sum()
                    ]
                }
                severity_df = pd.DataFrame(severity_data)
                
                plt.figure(figsize=(10, 6))
                sns.barplot(x='severity', y='count', hue='severity', data=severity_df, palette='YlOrRd', legend=False)
                plt.title('安防事件严重程度分布')
                plt.xlabel('严重程度')
                plt.ylabel('事件数量')
                plt.tight_layout()
                
                output_path = os.path.join(VISUALIZATION_DIR, 'security_events_by_severity.png')
                plt.savefig(output_path)
                plt.close()
                print(f"已保存安防事件严重程度分布图表到 {output_path}")
            
            # 可视化房屋面积与安防事件关系
            if 'square_meters' in df_events.columns and 'total_events' in df_events.columns:
                plt.figure(figsize=(10, 6))
                sns.scatterplot(x='square_meters', y='total_events', data=df_events)
                plt.title('房屋面积与安防事件数量关系')
                plt.xlabel('房屋面积 (平方米)')
                plt.ylabel('事件数量')
                
                # 添加趋势线
                sns.regplot(x='square_meters', y='total_events', data=df_events, scatter=False, ci=None, line_kws={"color":"red"})
                
                plt.tight_layout()
                
                output_path = os.path.join(VISUALIZATION_DIR, 'security_events_by_area.png')
                plt.savefig(output_path)
                plt.close()
                print(f"已保存房屋面积与安防事件关系图表到 {output_path}")
                
            # 可视化已解决与未解决事件比例
            if 'total_events' in df_events.columns and 'unresolved_events' in df_events.columns:
                # 计算已解决事件数量
                df_events['resolved_events'] = df_events['total_events'] - df_events['unresolved_events']
                
                # 创建饼图数据
                resolution_data = {
                    'status': ['已解决', '未解决'],
                    'count': [
                        df_events['resolved_events'].sum(),
                        df_events['unresolved_events'].sum()
                    ]
                }
                
                plt.figure(figsize=(8, 8))
                plt.pie(resolution_data['count'], labels=resolution_data['status'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
                plt.title('安防事件解决状态分布')
                plt.axis('equal')  # 确保饼图是圆的
                
                output_path = os.path.join(VISUALIZATION_DIR, 'security_events_resolution_status.png')
                plt.savefig(output_path)
                plt.close()
                print(f"已保存安防事件解决状态图表到 {output_path}")
        
    except Exception as e:
        print(f"警告: 安防事件可视化生成失败: {str(e)}")
        traceback.print_exc()  # 打印详细错误信息
        print("跳过安防事件可视化，继续其他图表生成")
        return

def visualize_user_feedback():
    """可视化用户反馈"""
    data = fetch_data_from_api("analytics/user-feedback-analysis")
    if not data:
        return
    
    # 打印数据类型和结构以便调试
    print(f"用户反馈数据类型: {type(data)}")
    
    # 检查数据格式
    if isinstance(data, list):
        df_feedback = pd.DataFrame(data)
        print(f"数据列: {df_feedback.columns.tolist()}")
        
        # 按反馈类型可视化
        if 'feedback_type' in df_feedback.columns and 'average_rating' in df_feedback.columns:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='feedback_type', y='average_rating', data=df_feedback)
            plt.title('不同类型反馈的平均评分')
            plt.xlabel('反馈类型')
            plt.ylabel('平均评分')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            output_path = os.path.join(VISUALIZATION_DIR, 'feedback_type_ratings.png')
            plt.savefig(output_path)
            plt.close()
            print(f"已保存反馈类型评分图表到 {output_path}")
        
        # 按月份可视化反馈量
        if 'month' in df_feedback.columns and 'year' in df_feedback.columns and 'total_feedbacks' in df_feedback.columns:
            # 创建时间列
            df_feedback['period'] = df_feedback.apply(lambda x: f"{int(x['year'])}-{int(x['month']):02d}", axis=1)
            
            plt.figure(figsize=(12, 6))
            sns.lineplot(x='period', y='total_feedbacks', data=df_feedback)
            plt.title('每月反馈数量趋势')
            plt.xlabel('时间')
            plt.ylabel('反馈数量')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            output_path = os.path.join(VISUALIZATION_DIR, 'feedback_monthly_trend.png')
            plt.savefig(output_path)
            plt.close()
            print(f"已保存月度反馈趋势图表到 {output_path}")
        
        # 响应率可视化
        if 'total_feedbacks' in df_feedback.columns and 'responded_count' in df_feedback.columns:
            # 计算响应率
            df_feedback['response_rate'] = df_feedback['responded_count'] / df_feedback['total_feedbacks'] * 100
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x='feedback_type', y='response_rate', data=df_feedback)
            plt.title('不同类型反馈的响应率')
            plt.xlabel('反馈类型')
            plt.ylabel('响应率 (%)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            output_path = os.path.join(VISUALIZATION_DIR, 'feedback_response_rate.png')
            plt.savefig(output_path)
            plt.close()
            print(f"已保存反馈响应率图表到 {output_path}")
            
            # 创建饼图显示反馈总量分布
            plt.figure(figsize=(8, 8))
            feedback_sum = df_feedback.groupby('feedback_type')['total_feedbacks'].sum()
            plt.pie(feedback_sum, labels=feedback_sum.index, autopct='%1.1f%%', startangle=90)
            plt.title('各类型反馈占比')
            plt.axis('equal')  # 确保饼图是圆的
            
            output_path = os.path.join(VISUALIZATION_DIR, 'feedback_type_distribution.png')
            plt.savefig(output_path)
            plt.close()
            print(f"已保存反馈类型分布图表到 {output_path}")
    else:
        print("警告: 用户反馈数据格式不符合预期")

def main():
    parser = argparse.ArgumentParser(description='智能家居系统数据可视化工具')
    parser.add_argument('--all', action='store_true', help='生成所有可视化图表')
    parser.add_argument('--usage-frequency', action='store_true', help='设备使用频率可视化')
    parser.add_argument('--usage-timeframe', action='store_true', help='设备使用时间段可视化')
    parser.add_argument('--usage-patterns', action='store_true', help='设备使用模式可视化')
    parser.add_argument('--home-area', action='store_true', help='房屋面积影响可视化')
    parser.add_argument('--security', action='store_true', help='安防事件可视化')
    parser.add_argument('--feedback', action='store_true', help='用户反馈可视化')
    
    args = parser.parse_args()
    
    # 如果没有指定任何参数，默认执行所有可视化
    if not any(vars(args).values()):
        args.all = True
    
    if args.all or args.usage_frequency:
        print("\n=== 正在生成设备使用频率可视化... ===")
        visualize_device_usage_frequency()
    
    if args.all or args.usage_timeframe:
        print("\n=== 正在生成设备使用时间段可视化... ===")
        visualize_device_usage_timeframe()
    
    if args.all or args.usage_patterns:
        print("\n=== 正在生成设备使用模式可视化... ===")
        visualize_device_usage_patterns()
    
    if args.all or args.home_area:
        print("\n=== 正在生成房屋面积影响可视化... ===")
        visualize_home_area_impact()
    
    if args.all or args.security:
        print("\n=== 正在生成安防事件可视化... ===")
        visualize_security_events()
    
    if args.all or args.feedback:
        print("\n=== 正在生成用户反馈可视化... ===")
        visualize_user_feedback()

if __name__ == "__main__":
    main()
