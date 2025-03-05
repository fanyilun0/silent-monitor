import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# Webhook配置 
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# 应用名称
APP_NAME = 'Silent Points Monitor'

# 代理配置
PROXY_URL = 'http://localhost:7890'
USE_PROXY = False
ALWAYS_NOTIFY = True

# 配置
API_URL = "https://ceremony-backend.silentprotocol.org/users/points"
TOKENS_FILE = "tokens.txt"
DATA_FILE = "points_data.json"
INTERVAL = 86400  # 24小时间隔

