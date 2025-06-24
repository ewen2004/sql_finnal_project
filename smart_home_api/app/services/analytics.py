from sqlalchemy.orm import Session
from sqlalchemy import func, text, and_, extract
from ..models.device_usage import DeviceUsage
from ..models.devices import Device, DeviceCategory
from ..models.homes import Home
from ..models.security_events import SecurityEvent
from ..models.feedback import Feedback
from typing import List, Dict, Any
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import logging

# 设置日志
logger = logging.getLogger(__name__)

def analyze_device_usage_frequency(db: Session):
    """分析设备使用频率"""
    try:
        # 直接使用原始SQL查询，而不依赖视图
        sql = """
        SELECT 
            d.device_id,
            d.device_name,
            dc.category_name,
            h.home_id,
            h.square_meters,
            COUNT(du.usage_id) as usage_count,
            SUM(EXTRACT(EPOCH FROM (du.end_time - du.start_time))/3600) as total_hours
        FROM devices d
        JOIN device_categories dc ON d.category_id = dc.category_id
        JOIN homes h ON d.home_id = h.home_id
        LEFT JOIN device_usage du ON d.device_id = du.device_id
        WHERE du.end_time IS NOT NULL
        GROUP BY d.device_id, d.device_name, dc.category_name, h.home_id, h.square_meters
        """
        
        result = db.execute(text(sql)).fetchall()
        
        # 转换为字典列表
        devices_usage = []
        for row in result:
            devices_usage.append({
                "device_id": row.device_id,
                "device_name": row.device_name,
                "category_name": row.category_name,
                "home_id": row.home_id,
                "square_meters": row.square_meters,
                "usage_count": row.usage_count,
                "total_hours": float(row.total_hours) if row.total_hours else 0
            })
        
        return devices_usage
    except Exception as e:
        logger.error(f"设备使用频率分析错误: {str(e)}")
        raise

def analyze_device_usage_timeframe(db: Session):
    """分析设备使用时间段"""
    try:
        # 直接使用SQL查询而不是视图
        sql = """
        SELECT 
            d.device_id,
            d.device_name,
            dc.category_name,
            EXTRACT(HOUR FROM du.start_time) as hour_of_day,
            COUNT(*) as usage_count
        FROM device_usage du
        JOIN devices d ON du.device_id = d.device_id
        JOIN device_categories dc ON d.category_id = dc.category_id
        GROUP BY d.device_id, d.device_name, dc.category_name, hour_of_day
        ORDER BY d.device_id, hour_of_day
        """
        
        result = db.execute(text(sql)).fetchall()
        
        # 转换为字典列表
        timeframes = []
        for row in result:
            timeframes.append({
                "device_id": row.device_id,
                "device_name": row.device_name,
                "category_name": row.category_name,
                "hour_of_day": int(row.hour_of_day),
                "usage_count": row.usage_count
            })
        
        return timeframes
    except Exception as e:
        logger.error(f"设备使用时间段分析错误: {str(e)}")
        raise

def analyze_device_usage_patterns(db: Session, min_support: float = 0.1):
    """分析设备使用模式（哪些设备经常一起使用）"""
    try:
        # 获取所有设备使用记录
        usage_records = db.query(
            DeviceUsage.usage_id,
            DeviceUsage.device_id,
            DeviceUsage.user_id,
            DeviceUsage.start_time,
            DeviceUsage.end_time,
            Device.device_name
        ).join(Device).all()
        
        # 检查数据是否足够
        if not usage_records or len(usage_records) < 10:
            return {"message": "没有足够的使用数据进行分析"}
        
        # 将记录转换为DataFrame
        df = pd.DataFrame([{
            "usage_id": r.usage_id,
            "device_id": r.device_id,
            "user_id": r.user_id,
            "start_time": r.start_time,
            "end_time": r.end_time or r.start_time,  # 如果end_time为空，使用start_time
            "device_name": r.device_name
        } for r in usage_records])
        
        if df.empty:
            return {"message": "没有足够的使用数据进行分析"}
        
        # 查找同时使用的设备
        # 为了简化，我们按照15分钟的时间窗口分组
        df['time_window'] = pd.to_datetime(df['start_time']).dt.floor('15min')
        
        # 创建透视表：每行是一个时间窗口，每列是一个设备，值为1表示该设备在该时间窗口内被使用
        basket = (df.groupby(['user_id', 'time_window', 'device_name'])['usage_id']
                .count().unstack().reset_index().fillna(0)
                .set_index(['user_id', 'time_window']))
        
        # 将计数转换为二进制（0或1）
        basket_sets = basket.map(lambda x: 1 if x > 0 else 0)
        
        # 如果数据不足，返回空结果
        if basket_sets.empty or len(basket_sets.columns) < 2:
            return {"message": "没有足够的数据生成关联规则"}
        
        try:
            # 使用Apriori算法找出频繁项集
            frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)
            
            # 如果没有找到频繁项集，返回空结果
            if frequent_itemsets.empty:
                return {"message": "未找到满足最小支持度的频繁项集"}
            
            # 根据频繁项集生成关联规则
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
            
            # 如果没有生成规则，返回空结果
            if rules.empty:
                return {"message": "未找到满足条件的关联规则"}
            
            # 将规则转换为更易读的格式
            formatted_rules = []
            for _, rule in rules.iterrows():
                antecedents = ', '.join(list(rule['antecedents']))
                consequents = ', '.join(list(rule['consequents']))
                formatted_rules.append({
                    "antecedents": antecedents,
                    "consequents": consequents,
                    "support": rule['support'],
                    "confidence": rule['confidence'],
                    "lift": rule['lift']
                })
            
            return {
                "rules": formatted_rules,
                "min_support": min_support
            }
        except Exception as e:
            logger.error(f"关联规则分析错误: {str(e)}")
            return {"message": f"分析设备使用模式时出错: {str(e)}"}
    except Exception as e:
        logger.error(f"设备使用模式分析错误: {str(e)}")
        raise

def analyze_home_area_impact(db: Session):
    """分析房屋面积对设备使用行为的影响"""
    try:
        sql = """
        SELECT 
            h.square_meters,
            h.num_rooms,
            d.device_id,
            d.device_name,
            dc.category_name,
            COUNT(du.usage_id) as usage_count,
            SUM(EXTRACT(EPOCH FROM (du.end_time - du.start_time))/3600) as total_hours
        FROM homes h
        JOIN devices d ON h.home_id = d.home_id
        JOIN device_categories dc ON d.category_id = dc.category_id
        LEFT JOIN device_usage du ON d.device_id = du.device_id
        WHERE du.end_time IS NOT NULL
        GROUP BY h.square_meters, h.num_rooms, d.device_id, d.device_name, dc.category_name
        ORDER BY h.square_meters
        """
        
        result = db.execute(text(sql)).fetchall()
        
        # 转换为字典列表
        area_impact = []
        for row in result:
            area_impact.append({
                "square_meters": float(row.square_meters),
                "num_rooms": row.num_rooms,
                "device_id": row.device_id,
                "device_name": row.device_name,
                "category_name": row.category_name,
                "usage_count": row.usage_count,
                "total_hours": float(row.total_hours) if row.total_hours else 0
            })
        
        return area_impact
    except Exception as e:
        logger.error(f"房屋面积影响分析错误: {str(e)}")
        raise

def analyze_security_events(db: Session):
    """分析安防事件"""
    try:
        sql = """
        SELECT 
            h.home_id,
            h.home_name,
            h.square_meters,
            COUNT(se.event_id) as total_events,
            COUNT(CASE WHEN se.is_resolved = FALSE THEN 1 END) as unresolved_events,
            COUNT(CASE WHEN se.severity = 'high' THEN 1 END) as high_severity_events,
            COUNT(CASE WHEN se.severity = 'medium' THEN 1 END) as medium_severity_events,
            COUNT(CASE WHEN se.severity = 'low' THEN 1 END) as low_severity_events
        FROM homes h
        LEFT JOIN security_events se ON h.home_id = se.home_id
        GROUP BY h.home_id, h.home_name, h.square_meters
        ORDER BY total_events DESC
        """
        
        result = db.execute(text(sql)).fetchall()
        
        # 转换为字典列表
        security_summary = []
        for row in result:
            security_summary.append({
                "home_id": row.home_id,
                "home_name": row.home_name,
                "square_meters": float(row.square_meters),
                "total_events": row.total_events,
                "unresolved_events": row.unresolved_events,
                "high_severity_events": row.high_severity_events,
                "medium_severity_events": row.medium_severity_events,
                "low_severity_events": row.low_severity_events
            })
        
        return security_summary
    except Exception as e:
        logger.error(f"安防事件分析错误: {str(e)}")
        raise

def analyze_user_feedback(db: Session):
    """分析用户反馈"""
    try:
        sql = """
        SELECT 
            feedback_type,
            AVG(rating) as average_rating,
            COUNT(*) as total_feedbacks,
            COUNT(CASE WHEN responded = TRUE THEN 1 END) as responded_count,
            EXTRACT(MONTH FROM created_at) as month,
            EXTRACT(YEAR FROM created_at) as year
        FROM feedbacks
        GROUP BY feedback_type, EXTRACT(MONTH FROM created_at), EXTRACT(YEAR FROM created_at)
        ORDER BY year, month
        """
        
        result = db.execute(text(sql)).fetchall()
        
        # 转换为字典列表
        feedback_analysis = []
        for row in result:
            feedback_analysis.append({
                "feedback_type": row.feedback_type,
                "average_rating": float(row.average_rating) if row.average_rating else 0,
                "total_feedbacks": row.total_feedbacks,
                "responded_count": row.responded_count,
                "month": int(row.month),
                "year": int(row.year)
            })
        
        return feedback_analysis
    except Exception as e:
        logger.error(f"用户反馈分析错误: {str(e)}")
        raise
