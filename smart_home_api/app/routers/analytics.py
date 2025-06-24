from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database import get_db
from ..services import analytics as service
import logging

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/device-usage-frequency")
def get_device_usage_frequency(db: Session = Depends(get_db)):
    """获取设备使用频率分析"""
    try:
        return service.analyze_device_usage_frequency(db)
    except Exception as e:
        logger.error(f"设备使用频率分析出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"设备使用频率分析出错: {str(e)}")

@router.get("/device-usage-timeframe")
def get_device_usage_timeframe(db: Session = Depends(get_db)):
    """获取设备使用时间段分析"""
    try:
        return service.analyze_device_usage_timeframe(db)
    except Exception as e:
        logger.error(f"设备使用时间段分析出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"设备使用时间段分析出错: {str(e)}")

@router.get("/device-usage-patterns")
def get_device_usage_patterns(min_support: float = 0.1, db: Session = Depends(get_db)):
    """分析设备使用模式（哪些设备经常一起使用）"""
    try:
        return service.analyze_device_usage_patterns(db, min_support)
    except Exception as e:
        logger.error(f"设备使用模式分析出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"设备使用模式分析出错: {str(e)}")

@router.get("/home-area-impact")
def get_home_area_impact(db: Session = Depends(get_db)):
    """分析房屋面积对设备使用行为的影响"""
    try:
        return service.analyze_home_area_impact(db)
    except Exception as e:
        logger.error(f"房屋面积影响分析出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"房屋面积影响分析出错: {str(e)}")

@router.get("/security-events-summary")
def get_security_events_summary(db: Session = Depends(get_db)):
    """获取安防事件摘要"""
    try:
        return service.analyze_security_events(db)
    except Exception as e:
        logger.error(f"安防事件摘要分析出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"安防事件摘要分析出错: {str(e)}")

@router.get("/user-feedback-analysis")
def get_user_feedback_analysis(db: Session = Depends(get_db)):
    """分析用户反馈"""
    try:
        return service.analyze_user_feedback(db)
    except Exception as e:
        logger.error(f"用户反馈分析出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"用户反馈分析出错: {str(e)}")
