# Silent-Monitor

一个灵活的自动化监控工具,可用于监控各类节点状态和数据变化。

## 功能特点

- 🔄 自动监控多个帐号积分
- 📱 企业微信机器人通知
- 🌐 支持代理配置
- ⏰ 可配置检查间隔
- 🐳 支持 Docker 部署

## 安装

### 方法一: 本地部署

1. 克隆仓库:
    ```bash
    git clone https://github.com/yourusername/silent-monitor.git
    cd silent-monitor
    ```

2. 安装依赖:
    ```bash
    pip install -r requirements.txt
    ```

3. 创建并配置 `.env` 文件:
    ```
    # 企业微信机器人配置
    WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=
    ```

4. 创建 `tokens.txt` 文件

5. 编辑 `config.py` 文件，根据需要修改以下参数:
    - `PROXY_URL`: 代理服务器地址（可选）
    - `USE_PROXY`: 是否启用代理
    - `INTERVAL`: 检查间隔时间（秒）


### 方法二: Docker 部署

1. 创建并配置 `.env` 文件（同上）

2. 使用 Docker Compose 启动:
    ```bash
    docker-compose up -d
    ```

Docker 环境变量说明:
- `TZ`: 时区设置，默认为 Asia/Shanghai
- `PYTHONUNBUFFERED`: Python 输出不缓冲
- `IS_DOCKER`: Docker 环境标识
- `HTTP_PROXY/HTTPS_PROXY`: 代理服务器配置

## 使用方法

### 本地运行:
```bash
python main.py
```

### Docker 运行:
```bash
# 查看日志
docker logs -f silent-monitor

# 重启服务
docker-compose restart

# 停止服务
docker-compose down
```


## 配置说明

### 帐号设置

- `tokens.txt`

### 环境变量 (.env)

- `WEBHOOK_URL`: 企业微信机器人的 webhook 地址

### 应用配置 (config.py)

- `PROXY_URL`: 代理服务器地址，默认为 http://localhost:7890
- `USE_PROXY`: 是否启用代理，默认为 False
- `INTERVAL`: 检查间隔时间（秒），默认为 10800（3小时）
- `TIME_OFFSET`: 时区偏移（小时），默认为 0

## 注意事项

- 请妥善保管配置信息，不要泄露给他人
- 建议使用代理以提高连接稳定性
- 可以根据需要调整检查间隔时间
- 如遇到问题，请查看程序输出的日志信息
- Docker 部署时注意配置正确的时区和代理设置

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持多目标监控
- 添加 Docker 部署支持
- 企业微信机器人通知集成