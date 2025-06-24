 # 智能家居管理系统 API

## 项目介绍

智能家居管理系统API提供了一套完整的RESTful接口，用于管理智能家居设备、用户、住宅以及相关数据分析。该系统支持设备监控、安防事件管理、用户反馈处理和使用数据分析等功能。

## 功能特点

- **用户管理**：注册、认证、个人信息管理
- **住宅管理**：添加、更新和删除住宅信息
- **设备管理**：智能设备注册、状态监控和控制
- **使用记录**：记录和查询设备使用历史
- **安防监控**：记录和处理安全事件
- **用户反馈**：收集和回复用户反馈
- **数据分析**：设备使用频率、能源消耗和使用模式分析

## 技术栈

- **后端框架**：FastAPI
- **数据库**：PostgreSQL
- **ORM**：SQLAlchemy
- **认证**：JWT令牌
- **API文档**：OpenAPI (Swagger/ReDoc)

## 快速开始

### 前置条件

- Python 3.8+
- PostgreSQL 12+

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/smart-home-api.git
cd smart-home-api
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 创建数据库：
```bash
# 连接到PostgreSQL
psql -U postgres

# 在PostgreSQL命令行中创建数据库
CREATE DATABASE smart_home_db;

# 退出
\q
```

5. 配置环境变量（创建.env文件）：
```
DATABASE_URL=postgresql://username:password@localhost/smart_home_db
SECRET_KEY=your_secret_key
```

6. 运行迁移并启动服务器：
```bash
# 初始化数据库
python -m app.initial_data

# 启动服务器
uvicorn app.main:app --reload
```

7.生成模拟数据：

python populate_test_data.py

8.可视化

python visualization.py

## API文档

启动服务器后，访问以下地址查看API文档：

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API使用指南

### 1. 用户管理

- 创建用户: `POST /users/`
- 获取用户信息: `GET /users/{user_id}`
- 更新用户信息: `PUT /users/{user_id}`
- 删除用户: `DELETE /users/{user_id}`
- 用户认证: `POST /users/login/`

### 2. 住宅管理

- 添加住宅: `POST /homes/`
- 获取住宅列表: `GET /homes/`
- 获取住宅详情: `GET /homes/{home_id}`
- 更新住宅信息: `PUT /homes/{home_id}`
- 删除住宅: `DELETE /homes/{home_id}`

### 3. 设备管理

- 添加设备: `POST /devices/`
- 获取设备列表: `GET /devices/`
- 获取设备详情: `GET /devices/{device_id}`
- 更新设备信息: `PUT /devices/{device_id}`
- 删除设备: `DELETE /devices/{device_id}`
- 控制设备: `POST /devices/{device_id}/control`

### 4. 设备使用记录

- 记录设备使用: `POST /device-usage/`
- 获取使用记录: `GET /device-usage/`
- 获取设备使用统计: `GET /device-usage/stats/{device_id}`

### 5. 安防事件

- 记录安全事件: `POST /security-events/`
- 获取安全事件列表: `GET /security-events/`
- 处理安全事件: `PUT /security-events/{event_id}`

### 6. 用户反馈

- 提交反馈: `POST /feedback/`
- 获取反馈列表: `GET /feedback/`
- 回复反馈: `PUT /feedback/{feedback_id}/respond`

### 7. 数据分析

- 获取设备使用频率: `GET /analytics/device-usage/`
- 获取能源消耗分析: `GET /analytics/energy-consumption/`
- 获取使用模式报告: `GET /analytics/usage-patterns/`

## 数据库结构

系统使用了以下主要数据表：

- `users`: 用户信息
- `homes`: 住宅信息
- `devices`: 设备信息
- `device_categories`: 设备类别
- `device_usage`: 设备使用记录
- `security_events`: 安全事件记录
- `feedbacks`: 用户反馈

## 贡献指南

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request


## 联系方式

项目维护者:17828025695@163.com.com
