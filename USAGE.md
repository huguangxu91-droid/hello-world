# AI Daily News - 使用指南 / Usage Guide

## 快速开始 / Quick Start

### 1. 获取最新新闻 / Fetch Latest News

```bash
python3 fetch_ai_news.py
```

这将获取最新的 AI 新闻并保存到 `ai_news_data.json` 文件。

### 2. 查看网页 / View the Web Page

#### 方法一：直接打开（Method 1: Direct Open）
直接在浏览器中打开 `index.html` 文件。

#### 方法二：使用本地服务器（Method 2: Use Local Server）
```bash
python3 -m http.server 8080
```

然后在浏览器中访问: http://localhost:8080/index.html

### 3. 设置定时更新 / Schedule Daily Updates

#### Linux/Mac (使用 crontab)

编辑 crontab：
```bash
crontab -e
```

添加以下行（每天早上8点更新）：
```bash
0 8 * * * cd /path/to/hello-world && ./schedule_daily_update.sh
```

或使用绝对路径：
```bash
0 8 * * * /path/to/hello-world/schedule_daily_update.sh
```

#### Windows (使用任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器为"每天"
4. 设置操作为运行脚本: `python fetch_ai_news.py`
5. 设置起始目录为项目目录

## 功能说明 / Features

### 网页功能 / Web Features
- ✅ 响应式设计，支持手机和电脑
- ✅ 自动刷新（每5分钟）
- ✅ 优雅的动画效果
- ✅ 显示新闻来源和时间
- ✅ 点击查看详细内容

### Python 脚本 / Python Script
- ✅ 自动获取 AI 相关新闻
- ✅ 保存为 JSON 格式
- ✅ 可扩展到真实新闻 API

## 扩展到真实 API / Extend to Real API

要使用真实的新闻 API（如 NewsAPI）：

1. 注册并获取 API Key: https://newsapi.org/

2. 设置环境变量：
```bash
export NEWS_API_KEY="your-api-key-here"
```

3. 修改 `fetch_ai_news.py` 中的相应代码，取消注释 API 调用部分。

## 文件结构 / File Structure

```
hello-world/
├── index.html              # 主页面
├── styles.css              # 样式文件
├── fetch_ai_news.py        # 新闻获取脚本
├── ai_news_data.json       # 新闻数据（自动生成）
├── schedule_daily_update.sh # 定时更新脚本
├── .gitignore              # Git 忽略文件
├── README.md               # 项目说明
└── USAGE.md                # 使用指南（本文件）
```

## 故障排除 / Troubleshooting

### 问题：网页显示"加载新闻失败"
**解决方案：**
1. 确认 `ai_news_data.json` 文件存在
2. 运行 `python3 fetch_ai_news.py` 生成数据
3. 使用本地服务器打开网页（避免 CORS 问题）

### 问题：Python 脚本运行失败
**解决方案：**
1. 确认 Python 3 已安装：`python3 --version`
2. 检查文件权限：`chmod +x fetch_ai_news.py`
3. 查看错误信息并根据提示修复

### 问题：定时任务没有执行
**解决方案：**
1. 检查 crontab 配置：`crontab -l`
2. 使用绝对路径
3. 查看系统日志：`grep CRON /var/log/syslog`

## 技术栈 / Tech Stack

- **前端**: HTML5, CSS3, JavaScript (Vanilla)
- **后端**: Python 3
- **数据格式**: JSON
- **样式**: CSS Grid, Flexbox, CSS Animations
- **兼容性**: 现代浏览器 (Chrome, Firefox, Safari, Edge)

## 许可证 / License

此项目为开源项目，可自由使用和修改。
