 # 智能家居管理系统 API部署与使用指南

## 介绍

智能家居管理系统API提供了一套完整的RESTful接口，用于管理智能家居设备、用户、住宅以及相关数据分析。该系统支持设备监控、安防事件管理、用户反馈处理和使用数据分析等功能。

## 数据库结构

系统使用了以下主要数据表：

- `users`: 用户信息
- `homes`: 住宅信息
- `devices`: 设备信息
- `device_categories`: 设备类别
- `device_usage`: 设备使用记录
- `security_events`: 安全事件记录
- `feedbacks`: 用户反馈

## 功能特点

- **用户管理**：注册、认证、个人信息管理
- **住宅管理**：添加、更新和删除住宅信息
- **设备管理**：智能设备注册、状态监控和控制
- **使用记录**：记录和查询设备使用历史
- **安防监控**：记录和处理安全事件
- **用户反馈**：收集和回复用户反馈
- **数据分析**：设备使用频率、能源消耗和使用模式等分析

## 1 环境配置与依赖安装

### 1.1 系统需求

在开始部署前，请确保系统满足以下要求：

- **操作系统**：支持 Linux、macOS 或 Windows
- **Python**：Python 3.8 或更高版本
- **PostgreSQL**：12.0 或更高版本
- **存储空间**：至少 500MB 可用空间（不包括数据库增长）
- **内存**：建议至少 4GB RAM

### 1.2 安装依赖

1. **安装项目依赖**

   ```bash
   pip install -r requirements.txt
   ```

   该命令将安装以下主要依赖：

   - FastAPI 和 Uvicorn 作为Web框架和服务器
   - SQLAlchemy 作为ORM工具
   - Psycopg2 用于PostgreSQL连接
   - 安全相关库（如python-jose、passlib和bcrypt）
   - 数据分析库（Pandas、NumPy、Matplotlib和Seaborn）
   - 关联规则挖掘库（MLxtend）

   安装过程中可能需要一些时间，特别是在安装数据分析相关库时。

## 2 数据库初始化

### 2.1 PostgreSQL安装与配置

如果尚未安装PostgreSQL，请按照以下步骤安装：

**对于Ubuntu/Debian：**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**对于macOS（使用Homebrew）：**

```bash
brew install postgresql
```

**对于Windows：**
从[PostgreSQL官方网站](https://www.postgresql.org/download/windows/)下载并安装。

### 2.2 创建数据库

1. **连接到PostgreSQL**

   ```bash
   sudo -u postgres psql  # Linux/macOS
   # 或在Windows上使用pgAdmin或命令行工具
   ```

2. **创建数据库**

   ```sql
   CREATE DATABASE smart_home_db;
   ```

3. **创建用户并授予权限**（可选，如果不想使用默认postgres用户）

   ```sql
   CREATE USER smart_home_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE smart_home_db TO smart_home_user;
   ```

### 2.3 配置数据库连接

1. **创建环境变量文件**

   修改项目根目录.env文件的密码：

   ```
   DATABASE_URL=postgresql://postgres:password（你的密码）@localhost/smart_home_db
   API_BASE_URL=http://localhost:8000/api
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   LOG_LEVEL=INFO
   ```

   请根据自己的数据库设置调整`DATABASE_URL`。格式为：`postgresql://用户名:密码@主机名/数据库名`

2. **初始化数据库表和基础数据**

   ```bash
   # 确保位于项目根目录下，smart_home_api\
   python -m app.initial_data
   ```

   此命令将：

   - 创建所有必要的数据表
   - 添加默认设备类别（照明设备、安防设备、环境控制等）

## 3 启动服务与测试

### 3.1 启动API服务

使用以下命令启动FastAPI服务器：

```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

成功启动后，将看到类似以下的输出：

```
INFO:     Started server process [28967]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3.2 生成测试数据

系统提供了一个便捷的脚本用于生成测试数据，以便快速体验系统功能。在服务器运行状态下，执行：

```bash
python populate_test_data.py
```

此脚本将生成：

- 100个测试用户
- 每个用户关联1个住宅
- 每个住宅有5个不同类型的设备
- 每个设备有5-50条使用记录
- 200条用户反馈
- 150条安防事件

测试数据生成过程可能需要几分钟时间，取决于系统性能。

### 3.3 验证系统运行状态

启动服务器后，可以通过以下URL访问系统：

- API根端点：http://127.0.0.1:8000/
- 健康检查：http://127.0.0.1:8000/health
- API文档（Swagger UI）：http://127.0.0.1:8000/docs

 ## 4 API使用示例

系统提供了一个交互式的API文档界面，可以方便地测试和使用所有API功能。

### 4.1 访问Swagger UI

当你启动服务器后，访问 http://127.0.0.1:8000/docs 就会打开Swagger UI界面，它提供了一个交互式的图形界面，让你可以：

1. 浏览所有可用的API端点
2. 查看每个API的详细参数说明
3. 直接在浏览器中填写参数并测试API调用
4. 查看API响应结果

### 4.2 用户管理API示例

**创建新用户**

1. 在Swagger UI中找到`POST /api/users/`端点

2. 点击"Try it out"按钮

3. 在请求体中填写用户信息（JSON格式）：

   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "phone": "13912345678",
     "password": "Password123!"
   }
   ```

4. 点击"Execute"执行请求

5. 直接在页面上查看响应结果

### 4.3 住宅管理API示例

**添加住宅**

1. 在Swagger UI中找到`POST /api/homes/`端点

2. 点击"Try it out"按钮

3. 在请求体中填写住宅信息：

   ```json
   {
     "user_id": 1,
     "home_name": "我的智能公寓",
     "address": "北京市海淀区中关村大街1号",
     "square_meters": 120.5,
     "num_rooms": 3
   }
   ```

4. 点击"Execute"执行请求

### 4.4 设备管理API示例

**添加设备**

1. 在Swagger UI中找到`POST /api/devices/`端点

2. 点击"Try it out"按钮

3. 在请求体中填写设备信息：

   ```json
   {
     "home_id": 1,
     "category_id": 1,
     "device_name": "客厅智能灯",
     "model": "Philips Hue A19",
     "manufacturer": "Philips",
     "room_location": "客厅"
   }
   ```

4. 点击"Execute"执行请求

### 4.5 数据分析API示例

**设备使用频率分析**

1. 在Swagger UI中找到`GET /api/analytics/device-usage-frequency`端点
2. 点击"Try it out"按钮
3. 不需要填写任何参数，直接点击"Execute"
4. 查看返回的分析结果

这种方式比使用curl命令更直观，特别适合初次使用API的人，因为它不需要记忆复杂的命令语法，并且提供了良好的文档支持。系统还定制了Swagger UI的样式（通过`swagger-ui-custom.css`），使界面更加美观和易用。

## 5 数据可视化操作指南

系统提供了专门的可视化工具，用于将API返回的数据转换为直观的图表。

### 5.1 运行可视化脚本

在项目根目录下，使用以下命令运行可视化脚本：

```bash
# 生成所有类型的可视化
python visualization.py --all

# 或者生成特定类型的可视化
python visualization.py --usage-frequency --usage-timeframe
```

可用的命令行参数包括：

- `--all`：生成所有可视化图表
- `--usage-frequency`：设备使用频率可视化
- `--usage-timeframe`：设备使用时间段可视化
- `--usage-patterns`：设备使用模式可视化
- `--home-area`：房屋面积影响可视化
- `--security`：安防事件可视化
- `--feedback`：用户反馈可视化

### 5.2 查看生成的可视化

可视化图表将保存在项目根目录下的`visualizations`文件夹中。您可以使用任何图像查看器查看这些PNG格式的图表。

主要的可视化图表包括：

1. **设备使用频率图表**
   - `device_usage_frequency.png`：各设备使用次数柱状图
   - `device_usage_duration.png`：各设备使用时长柱状图
2. **设备使用时间段图表**
   - `device_usage_timeframe.png`：设备与时间的热力图
   - 针对每个设备的单独时间分布图
3. **设备使用模式图表**
   - `device_usage_patterns.png`：设备使用关联规则散点图
4. **房屋面积影响图表**
   - `home_area_impact_count.png`：面积与使用次数关系图
   - `home_area_impact_hours.png`：面积与使用时长关系图
   - 针对各设备类别的单独分析图
5. **安防事件图表**
   - `security_events_by_home.png`：各住宅安防事件分布
   - `security_events_by_severity.png`：事件严重程度分布
   - `security_events_by_area.png`：面积与事件数量关系
   - `security_events_resolution_status.png`：事件解决状态饼图
6. **用户反馈图表**
   - `feedback_type_ratings.png`：不同类型反馈的评分
   - `feedback_monthly_trend.png`：月度反馈趋势
   - `feedback_response_rate.png`：反馈响应率
   - `feedback_type_distribution.png`：反馈类型分布饼图

### 5.3 自定义可视化

如果需要创建自定义的可视化，可以通过以下步骤实现：

1. **获取API数据**：使用requests库从API获取数据
2. **数据处理**：使用pandas处理和转换数据
3. **创建图表**：使用matplotlib或seaborn创建可视化图表

示例代码：

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt

# 获取API数据
response = requests.get('http://127.0.0.1:8000/api/analytics/device-usage-frequency')
data = response.json()

# 转换为DataFrame
df = pd.DataFrame(data)

# 创建自定义图表
plt.figure(figsize=(12, 8))
plt.bar(df['device_name'], df['usage_count'], color='skyblue')
plt.title('设备使用频率分析 - 自定义图表')
plt.xlabel('设备名称')
plt.ylabel('使用次数')
plt.xticks(rotation=45)
plt.tight_layout()

# 保存图表
plt.savefig('my_custom_visualization.png')
```

### 5.4 在网络中展示可视化

可以通过简单的HTTP服务器在网络中展示生成的可视化图表：

```bash
# 切换到visualizations目录
cd visualizations

# 启动Python内置的HTTP服务器
python -m http.server 8080
```

然后通过浏览器访问`http://localhost:8080`即可查看和下载所有生成的可视化图表。
