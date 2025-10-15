# hello-world
my first project
some changes

## AI 每日新闻 / AI Daily News

这是一个用于收集和展示每日 AI 最新前沿新闻的功能。

### 功能特点

- 🤖 自动获取最新的 AI 相关新闻
- 📱 响应式网页设计，支持桌面和移动设备
- 🎨 现代化的用户界面
- 🔄 自动刷新功能（每5分钟）
- 📊 显示新闻来源和发布时间

### 使用方法

1. **获取最新新闻**
   ```bash
   python3 fetch_ai_news.py
   ```

2. **查看新闻页面**
   
   打开 `index.html` 文件在浏览器中查看，或使用本地服务器：
   ```bash
   python3 -m http.server 8080
   ```
   然后访问: http://localhost:8080/index.html

### 文件说明

- `index.html` - 新闻展示页面（主页）
- `styles.css` - 页面样式文件
- `fetch_ai_news.py` - 新闻获取脚本
- `ai_news_data.json` - 新闻数据存储文件

### 自动化更新

要设置每日自动更新，可以使用 cron job（Linux/Mac）或任务计划程序（Windows）：

**Linux/Mac (crontab):**
```bash
# 每天早上 8:00 运行
0 8 * * * cd /path/to/hello-world && python3 fetch_ai_news.py
```

**Windows (任务计划程序):**
创建一个每日任务来执行 `fetch_ai_news.py` 脚本。

### 扩展功能

如果要使用真实的新闻 API（如 NewsAPI），需要：
1. 注册获取 API Key
2. 设置环境变量 `NEWS_API_KEY`
3. 修改 `fetch_ai_news.py` 中的相应代码

### 截图

![AI 每日新闻页面](https://github.com/user-attachments/assets/6e963710-3962-4a75-ab5c-522d0b03eb3d)
