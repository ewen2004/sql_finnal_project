from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import User, Home, DeviceCategory, Device
import bcrypt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建所有表
def init_db():
    logger.info("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建完成")

# 添加默认设备类别
def create_device_categories(db: Session):
    logger.info("正在添加默认设备类别...")
    
    categories = [
        {"category_name": "照明设备", "description": "各类智能灯具，包括吸顶灯、台灯、落地灯等"},
        {"category_name": "安防设备", "description": "监控摄像头、门窗传感器、智能门锁等安全设备"},
        {"category_name": "环境控制", "description": "空调、暖气、新风系统等环境控制设备"},
        {"category_name": "厨房电器", "description": "智能冰箱、烤箱、微波炉等厨房设备"},
        {"category_name": "娱乐设备", "description": "智能电视、音响、投影仪等娱乐设备"},
        {"category_name": "清洁设备", "description": "扫地机器人、洗碗机等自动清洁设备"}
    ]
    
    for cat_data in categories:
        # 检查类别是否已存在
        existing = db.query(DeviceCategory).filter(DeviceCategory.category_name == cat_data["category_name"]).first()
        if not existing:
            category = DeviceCategory(**cat_data)
            db.add(category)
    
    db.commit()
    logger.info(f"已添加{len(categories)}个设备类别")

def main():
    logger.info("开始初始化数据库...")
    
    # 创建数据库表
    init_db()
    
    # 添加初始数据
    db = SessionLocal()
    try:
        create_device_categories(db)
    finally:
        db.close()
    
    logger.info("数据库初始化完成")

if __name__ == "__main__":
    main()
