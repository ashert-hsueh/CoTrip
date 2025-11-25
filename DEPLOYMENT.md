# 部署说明

## 环境要求

### 前端
- Node.js >= 16.0.0
- npm >= 8.0.0

### 后端
- Python >= 3.9.0
- pip >= 21.0.0

## 安装与运行

### 1. 安装依赖

#### 前端
```bash
cd frontend
npm install
```

#### 后端
```bash
cd backend
python -m pip install -r requirements.txt
```

### 2. 配置环境变量

#### 前端
复制环境变量示例文件并配置：
```bash
cd frontend
cp .env.example .env
```

编辑 `.env` 文件，填入高德地图API密钥：
```env
# 高德地图API配置
# 请在高德开放平台申请API密钥：https://console.amap.com/dev/index
VITE_AMAP_KEY=your_amap_web_api_key_here
VITE_AMAP_SECRET=your_amap_web_api_secret_here

# 后端API地址（开发环境）
VITE_API_BASE_URL=http://localhost:8000
```

### 3. 启动服务

#### 启动后端服务（Terminal 1）
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将启动在：http://localhost:8000

#### 启动前端服务（Terminal 2）
```bash
cd frontend
npm run dev
```

前端服务将启动在：http://localhost:5173

## 访问应用

在浏览器中访问：http://localhost:5173

## 功能测试

### 旅行管理功能测试

1. **旅行规划页面**
   - 检查是否显示旅行本瀑布流布局（一行5个旅行本）
   - 验证旅行本封面样式（默认色#70CDE5，华文行楷字体）
   - 测试点击旅行本是否显示翻开动画
   - 检查右侧是否有"新建旅行本"按钮

2. **旅行本详情页面**
   - 验证面包屑导航是否正常（我的旅行本 → 旅行本标题）
   - 检查地图组件是否正常加载
   - 测试地点搜索功能：
     - 输入目的地名称进行搜索
     - 点击搜索结果是否能添加到地图标记
   - 测试路线规划功能：
     - 选择起点和终点
     - 切换交通方式（步行/驾车/公共交通/骑行）
     - 验证路线是否正确显示在地图上

3. **高德地图API功能**
   - 确认地图能正常显示
   - 验证地点标记功能
   - 测试路线计算和显示

## 常见问题

### Q: 高德地图加载失败
A: 请检查：
1. `.env` 文件中的 `VITE_AMAP_KEY` 是否正确配置
2. 网络连接是否正常
3. API密钥是否在高德开放平台已启用Web端服务

### Q: 前端无法连接后端
A: 请检查：
1. 后端服务是否正常启动在端口8000
2. `.env` 文件中的 `VITE_API_BASE_URL` 是否正确
3. 防火墙或代理设置是否允许连接

### Q: 依赖安装失败
A: 尝试清理缓存后重新安装：
#### 前端
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 后端
```bash
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 生产部署

### 前端构建
```bash
cd frontend
npm run build
```

构建产物将生成在 `dist` 目录。

### 后端部署
建议使用 `gunicorn` 作为生产服务器：
```bash
cd backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 技术支持

如遇到问题，请检查：
1. 所有依赖是否正确安装
2. 环境变量是否正确配置
3. 端口是否被占用
4. 网络连接是否正常