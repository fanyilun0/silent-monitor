import asyncio
import aiohttp
from datetime import datetime
import logging
import json
import os

# 导入配置
from config import (
    API_URL,
    TOKENS_FILE,
    DATA_FILE,
    WEBHOOK_URL,
    PROXY_URL,
    USE_PROXY,
    INTERVAL,
    APP_NAME,
)

# 配置logging
def setup_logging():
    """配置日志格式和级别"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# 在导入配置后添加
logger.info(f"当前使用的代理URL: {PROXY_URL if USE_PROXY else '未使用代理'}")

def load_tokens():
    """从文件加载tokens,返回{token_id: token}格式的字典"""
    tokens_dict = {}
    try:
        with open(TOKENS_FILE, 'r') as f:
            for line in f:
                token = line.strip()
                if token:
                    # 使用token末尾4位作为标识
                    token_id = token[-4:]
                    tokens_dict[token_id] = token
        return tokens_dict
    except Exception as e:
        logger.error(f"加载tokens失败: {str(e)}")
        return {}

def save_data(data):
    """保存数据到json文件"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"数据已保存到 {DATA_FILE}")
    except Exception as e:
        logger.error(f"保存数据失败: {str(e)}")

async def fetch_data_with_token(session, token, token_id, index):
    """使用token获取API数据"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        proxy = PROXY_URL if USE_PROXY else None
        timeout = aiohttp.ClientTimeout(total=20)
        async with session.get(API_URL, 
                             headers=headers, 
                             ssl=False, 
                             proxy=proxy,
                             timeout=timeout) as response:
            if response.status == 200:
                logger.info(f"✅ 账号{index} Token[{token_id}] - 请求状态: {response.status}")
                data = await response.json()
                return data
            else:
                logger.error(f"❌ 账号{index} Token[{token_id}] - 获取数据失败: {response.status}")
                return None
    except Exception as e:
        logger.error(f"❌ 账号{index} Token[{token_id}] - 请求出错: {str(e)}")
        return None

def build_points_message(accounts_data):
    """构建所有账号的积分消息"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    message_lines = [
        f"🔍 【{APP_NAME} - Points Update】",
        f"⏰ 时间: {timestamp}\n"
    ]
    
    for i, account in enumerate(accounts_data):
        name = account['name']
        points_data = account['data']
        message_lines.extend([
            f"👤 账号{i}: {name}",
            f"🏆 Points: {points_data.get('points', '未知')}",
            f"📈 其他数据: {json.dumps(points_data, indent=2)}\n"
        ])
    
    return "\n".join(message_lines)

async def send_message_async(webhook_url, message_content, use_proxy, proxy_url):
    """发送消息到webhook"""
    headers = {'Content-Type': 'application/json'}
    payload = {
        "msgtype": "text",
        "text": {
            "content": message_content
        }
    }
    
    proxy = proxy_url if use_proxy else None
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(webhook_url, json=payload, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    logger.info("消息发送成功!")
                else:
                    logger.error(f"发送消息失败: {response.status}")
        except Exception as e:
            logger.error(f"发送消息出错: {str(e)}")

async def monitor_points():
    """主监控函数"""
    iteration = 1
    
    while True:
        try:
            logger.info(f"\n🔄 开始第 {iteration} 轮检查...")
            
            tokens_dict = load_tokens()
            if not tokens_dict:
                logger.error("❌ 没有找到可用的tokens")
                await asyncio.sleep(INTERVAL)
                continue
                
            all_data = {
                'timestamp': datetime.now().isoformat(),
                'points_data': []
            }
            
            async with aiohttp.ClientSession() as session:
                for i, (token_id, token) in enumerate(tokens_dict.items()):
                    data = await fetch_data_with_token(session, token, token_id, i)
                    if data:
                        data_with_id = {
                            'name': f'Token[{token_id}]',
                            'data': data
                        }
                        all_data['points_data'].append(data_with_id)
                    await asyncio.sleep(1)
                
                if all_data['points_data']:
                    # 构建并发送合并后的消息
                    message = build_points_message(all_data['points_data'])
                    await send_message_async(WEBHOOK_URL, message, USE_PROXY, PROXY_URL)
                    save_data(all_data)
            
            logger.info(f"✨ 第 {iteration} 轮检查完成\n")
            iteration += 1
            
        except Exception as e:
            logger.error(f"❌ 监控过程出错: {str(e)}")
            
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(monitor_points())