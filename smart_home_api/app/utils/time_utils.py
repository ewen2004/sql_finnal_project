from datetime import datetime, timedelta
import pytz

def get_local_time(timezone_str: str = "Asia/Shanghai"):
    """获取指定时区的当前时间"""
    tz = pytz.timezone(timezone_str)
    return datetime.now(tz)

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S"):
    """格式化日期时间"""
    return dt.strftime(format_str)

def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S"):
    """解析日期时间字符串"""
    return datetime.strptime(dt_str, format_str)

def get_time_range(days: int = 7):
    """获取从现在到过去几天的时间范围"""
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    return start_time, end_time

def get_hour_of_day(dt: datetime):
    """获取一天中的小时"""
    return dt.hour

def get_day_of_week(dt: datetime):
    """获取星期几，0表示星期一，6表示星期日"""
    return dt.weekday()
