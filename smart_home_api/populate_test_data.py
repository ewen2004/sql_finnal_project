import requests
import random
import time
from datetime import datetime, timedelta
import json

# API基础URL
BASE_URL = "http://127.0.0.1:8000/api"

# 模拟数据量
NUM_USERS = 100
NUM_HOMES_PER_USER = 1  # 每个用户的住宅数
NUM_DEVICES_PER_HOME = 5  # 每个住宅的设备数
# 为每个设备生成随机数量的使用记录
MIN_USAGE_RECORDS = 5    # 最少记录数
MAX_USAGE_RECORDS = 50   # 最多记录数

NUM_FEEDBACK = 200  # 总反馈数
NUM_SECURITY_EVENTS = 150  # 总安全事件数

# 随机数据生成辅助函数
def random_phone():
    return f"13{random.randint(1, 9)}{random.randint(100, 999)}{random.randint(1000, 9999)}"

def random_address():
    cities = ["北京市", "上海市", "广州市", "深圳市", "杭州市", "成都市", "武汉市", "南京市"]
    districts = ["朝阳区", "海淀区", "浦东新区", "天河区", "西湖区", "锦江区", "江夏区", "建邺区"]
    streets = ["中关村大街", "长安街", "南京路", "天河路", "西湖大道", "春熙路", "解放大道", "秦淮路"]
    return f"{random.choice(cities)}{random.choice(districts)}{random.choice(streets)}{random.randint(1, 100)}号"

def random_device_name(category_name):
    prefixes = {
        "照明设备": ["智能", "自动", "声控", "遥控", "节能"],
        "安防设备": ["高清", "红外", "智能", "监控", "防盗"],
        "环境控制": ["温控", "智能", "静音", "节能", "舒适"],
        "厨房电器": ["智能", "多功能", "节能", "自动", "高效"],
        "娱乐设备": ["智能", "高清", "无线", "环绕", "超薄"],
        "清洁设备": ["自动", "智能", "无线", "超静音", "高效"]
    }
    
    names = {
        "照明设备": ["吸顶灯", "台灯", "落地灯", "壁灯", "灯带"],
        "安防设备": ["摄像头", "门锁", "传感器", "报警器", "智能门铃"],
        "环境控制": ["空调", "加湿器", "新风机", "温控器", "空气净化器"],
        "厨房电器": ["冰箱", "烤箱", "微波炉", "洗碗机", "电饭煲"],
        "娱乐设备": ["电视", "音响", "投影仪", "游戏机", "智能音箱"],
        "清洁设备": ["扫地机器人", "洗衣机", "干衣机", "吸尘器", "洗地机"]
    }
    
    prefix = random.choice(prefixes.get(category_name, ["智能"]))
    name = random.choice(names.get(category_name, ["设备"]))
    return f"{prefix}{name}"

def random_manufacturer():
    return random.choice(["小米", "华为", "苹果", "三星", "格力", "海尔", "西门子", "飞利浦", "松下", "博世"])

def random_model():
    return f"Model-{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}{random.randint(100, 999)}"

def random_room():
    return random.choice(["客厅", "卧室", "厨房", "书房", "浴室", "餐厅", "阳台"])

def random_feedback_content():
    positive = [
        "设备运行良好，界面简洁明了。",
        "连接稳定，使用体验很好。",
        "功能很全面，满足了我的需求。",
        "设计精美，与家居风格很搭配。",
        "操作简单，老人小孩都能轻松使用。"
    ]
    
    neutral = [
        "设备功能基本满足需求，但有待改进。",
        "连接偶尔不稳定，但总体满意。",
        "功能很全面，但启动速度有点慢。",
        "设计不错，但材质可以更好一些。",
        "使用方便，但说明书不够详细。"
    ]
    
    negative = [
        "设备经常断连，影响使用体验。",
        "功能太少，不值这个价格。",
        "设计不合理，操作很不方便。",
        "噪音太大，晚上根本无法使用。",
        "耗电量大，不够节能环保。"
    ]
    
    feedback_type = random.choice(["positive", "neutral", "negative"])
    if feedback_type == "positive":
        return random.choice(positive)
    elif feedback_type == "neutral":
        return random.choice(neutral)
    else:
        return random.choice(negative)

def random_event_type():
    return random.choice(["异常访问", "设备离线", "异常操作", "电量告警", "网络异常", "系统更新", "传感器告警"])

def random_event_description(event_type):
    descriptions = {
        "异常访问": [
            "检测到未知IP地址尝试访问设备",
            "多次错误密码尝试登录",
            "检测到可疑的访问模式",
            "非常规时间段的访问尝试"
        ],
        "设备离线": [
            "设备突然断开连接",
            "设备超过24小时未上线",
            "设备反复上下线",
            "设备无响应需要重启"
        ],
        "异常操作": [
            "短时间内频繁操作设备",
            "非常规操作序列",
            "检测到可能的误操作",
            "未授权的设备控制请求"
        ],
        "电量告警": [
            "设备电量低于20%",
            "电池电量异常下降",
            "设备即将关闭",
            "需要更换电池"
        ],
        "网络异常": [
            "设备网络连接不稳定",
            "网络延迟异常",
            "数据包丢失率高",
            "设备无法连接到路由器"
        ],
        "系统更新": [
            "系统更新失败",
            "固件升级中断",
            "系统需要重要安全更新",
            "检测到新版本可用"
        ],
        "传感器告警": [
            "温度传感器检测到异常高温",
            "湿度传感器数值超出正常范围",
            "运动传感器检测到异常活动",
            "烟雾传感器触发警报"
        ]
    }
    return random.choice(descriptions.get(event_type, ["系统检测到异常"]))

def random_severity():
    return random.choice(["low", "medium", "high", "critical"])

# 创建测试数据
def create_test_data():
    print("开始创建测试数据...")
    
    # 存储创建的数据ID
    users = []
    homes = []
    devices = []
    
    # 1. 获取设备类别
    response = requests.get(f"{BASE_URL}/devices/categories/")
    categories = response.json() if response.status_code == 200 else []
    
    if not categories:
        print("获取设备类别失败，无法继续")
        return
    
    print(f"获取到{len(categories)}个设备类别")
    
    # 2. 创建用户
    print(f"创建{NUM_USERS}个测试用户...")
    for i in range(NUM_USERS):
        timestamp = int(time.time())
        username = f"testuser_{timestamp}_{i}"
        email = f"test_{timestamp}_{i}@example.com"
        phone = random_phone()
        
        user_data = {
            "username": username,
            "email": email,
            "phone": phone,
            "password": "Password123!"
        }
        
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 201:
            user = response.json()
            users.append(user["user_id"])
            print(f"  创建用户: {username} (ID: {user['user_id']})")
        else:
            print(f"  创建用户失败: {response.text}")
    
    # 3. 为每个用户创建住宅
    print("创建测试住宅...")
    for user_id in users:
        for i in range(NUM_HOMES_PER_USER):
            home_data = {
                "user_id": user_id,
                "home_name": f"测试住宅_{user_id}_{i}",
                "address": random_address(),
                "square_meters": random.uniform(50, 200),
                "num_rooms": random.randint(1, 5)
            }
            
            response = requests.post(f"{BASE_URL}/homes/", json=home_data)
            if response.status_code == 201:
                home = response.json()
                homes.append(home["home_id"])
                print(f"  创建住宅: {home_data['home_name']} (ID: {home['home_id']})")
            else:
                print(f"  创建住宅失败: {response.text}")
    
    # 4. 为每个住宅创建设备
    print("创建测试设备...")
    for home_id in homes:
        # 为每个住宅随机选择几个不同类别的设备
        selected_categories = random.sample(categories, min(len(categories), NUM_DEVICES_PER_HOME))
        
        for category in selected_categories:
            device_data = {
                "home_id": home_id,
                "category_id": category["category_id"],
                "device_name": random_device_name(category["category_name"]),
                "model": random_model(),
                "manufacturer": random_manufacturer(),
                "room_location": random_room()
            }
            
            response = requests.post(f"{BASE_URL}/devices/", json=device_data)
            if response.status_code == 201:
                device = response.json()
                devices.append(device["device_id"])
                print(f"  创建设备: {device_data['device_name']} (ID: {device['device_id']})")
            else:
                print(f"  创建设备失败: {response.text}")

    # 5. 创建设备使用记录
    print("创建设备使用记录...")
    for device_id in devices:
        # 为每个设备随机选择一个用户
        user_id = random.choice(users)
        
        # 为每个设备随机生成不同数量的记录
        num_records = random.randint(MIN_USAGE_RECORDS, MAX_USAGE_RECORDS)

        # 创建多条使用记录，时间从过去30天到现在
        for i in range(num_records):
            # 随机开始时间（过去30天内）
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            
            start_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # 使用时长（10分钟到4小时）
            usage_duration = timedelta(minutes=random.randint(10, 240))
            end_time = start_time + usage_duration
            
            # 如果结束时间超过当前时间，则设为当前时间
            if end_time > datetime.now():
                end_time = datetime.now()
            
            usage_data = {
                "device_id": device_id,
                "user_id": user_id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "operation_type": random.choice(["开启", "调节", "设置", "监控", "关闭"]),
                "operation_value": str(random.randint(1, 100))
            }
            
            response = requests.post(f"{BASE_URL}/device-usage/", json=usage_data)
            if response.status_code != 201:
                print(f"  创建使用记录失败: {response.text}")
    
    print(f"已为{len(devices)}个设备创建使用记录")
    
    # 6. 创建用户反馈
    print("创建用户反馈...")
    for i in range(NUM_FEEDBACK):
        user_id = random.choice(users)
        
        feedback_data = {
            "user_id": user_id,
            "feedback_type": random.choice(["bug", "feature", "general", "support"]),
            "content": random_feedback_content(),
            "rating": random.randint(1, 5)
        }
        
        response = requests.post(f"{BASE_URL}/feedback/", json=feedback_data)
        if response.status_code != 201:
            print(f"  创建反馈失败: {response.text}")
    
    print(f"已创建{NUM_FEEDBACK}条用户反馈")
    
    # 7. 创建安全事件
    print("创建安全事件...")
    for i in range(NUM_SECURITY_EVENTS):
        home_id = random.choice(homes)
        device_id = random.choice(devices) if random.random() > 0.3 else None  # 30%的事件不关联设备
        
        event_type = random_event_type()
        
        security_event_data = {
            "home_id": home_id,
            "device_id": device_id,
            "event_type": event_type,
            "severity": random_severity(),
            "description": random_event_description(event_type)
        }
        
        response = requests.post(f"{BASE_URL}/security-events/", json=security_event_data)
        if response.status_code != 201:
            print(f"  创建安全事件失败: {response.text}")
    
    print(f"已创建{NUM_SECURITY_EVENTS}条安全事件")
    
    print("测试数据创建完成！")

if __name__ == "__main__":
    create_test_data()
