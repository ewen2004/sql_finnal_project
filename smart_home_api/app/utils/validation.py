import re
from typing import Optional

def validate_email(email: str) -> bool:
    """验证电子邮件格式"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """验证手机号码格式（中国大陆）"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_ip_address(ip: str) -> bool:
    """验证IP地址格式"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    # 检查每个部分是否在0-255范围内
    parts = ip.split('.')
    for part in parts:
        if int(part) > 255:
            return False
    
    return True

def validate_mac_address(mac: str) -> bool:
    """验证MAC地址格式"""
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, mac))

def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    验证密码强度
    
    要求：
    - 至少8个字符
    - 至少包含一个数字
    - 至少包含一个大写字母
    - 至少包含一个小写字母
    - 至少包含一个特殊字符
    
    返回：
    - (是否通过, 错误消息)
    """
    if len(password) < 8:
        return False, "密码长度不能少于8个字符"
    
    if not re.search(r'\d', password):
        return False, "密码必须包含至少一个数字"
    
    if not re.search(r'[A-Z]', password):
        return False, "密码必须包含至少一个大写字母"
    
    if not re.search(r'[a-z]', password):
        return False, "密码必须包含至少一个小写字母"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "密码必须包含至少一个特殊字符"
    
    return True, None
