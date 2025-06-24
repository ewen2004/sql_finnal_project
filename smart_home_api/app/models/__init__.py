# 首先导入没有依赖关系的基础模型
from .users import User
from .homes import Home
from .devices import DeviceCategory, Device
from .feedback import Feedback
from .device_usage import DeviceUsage
from .security_events import SecurityEvent

# 确保所有模型都已加载和注册
