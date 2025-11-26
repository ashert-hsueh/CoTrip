# CoTrip - 协同旅行规划平台

## 🌟 项目简介

CoTrip 是一个现代化的协同旅行规划平台，帮助用户轻松规划旅行路线、管理旅行预算和账单。

## ✨ 主要功能

### 🗺️ 旅行规划
- 交互式地图路线规划
- 目的地管理
- 行程安排

### 💰 账本管理
- 创建和管理多个账本
- 多人协同管理
- 旅行计划关联

### 🧾 账单记录
- 多种账单类型（住宿、餐饮、交通、门票、其他）
- 详细的费用记录
- 智能拆账功能

### 👥 用户管理
- 用户注册和登录
- 个人信息管理
- 权限控制

## 🚀 快速开始

### 环境要求
- **Python**: 3.8+
- **Node.js**: 16+
- **npm**: 8+

### 方法一：一键启动（推荐）

**使用PowerShell启动所有服务：**
```powershell
.\start_all.ps1
```

### 方法二：分别启动

**启动后端服务：**
```powershell
python start_backend.py
```

**启动前端服务：**
```powershell
.\start_frontend.ps1
```

或者在cmd中：
```cmd
start_frontend.bat
```

### 方法三：手动启动

**启动后端：**
```bash
cd backend
pip install fastapi uvicorn sqlalchemy passlib python-multipart
python main.py
```

**启动前端：**
```bash
cd frontend
npm install
npm run dev
```

## 📱 访问应用

启动完成后，在浏览器中访问：
- **前端应用**: `http://localhost:5173`
- **后端API**: `http://localhost:8000`
- **API文档**: `http://localhost:8000/docs`

## 🛠️ 技术栈

### 前端技术
- **Vue 3**: 渐进式JavaScript框架
- **TypeScript**: 类型安全的JavaScript超集
- **Element Plus**: 基于Vue 3的UI组件库
- **Vue Router**: Vue官方路由管理器
- **Pinia**: Vue官方状态管理库
- **Vite**: 下一代前端构建工具
- **Axios**: HTTP客户端

### 后端技术
- **FastAPI**: 现代、快速的Web框架
- **Python**: 强大的编程语言
- **SQLAlchemy**: SQL工具包和ORM
- **SQLite**: 轻量级数据库
- **Passlib**: 密码哈希库
- **Uvicorn**: ASGI服务器

## 📁 项目结构

```
CoTrip/
├── backend/                 # 后端代码
│   ├── application/        # 应用层（业务逻辑）
│   ├── database/           # 数据库层（ORM实体）
│   ├── persistence/        # 持久化层（数据访问）
│   ├── presentation/       # 表示层（API路由）
│   └── main.py            # 主应用入口
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API客户端
│   │   ├── components/    # Vue组件
│   │   ├── pages/         # 页面组件
│   │   ├── router/        # 路由配置
│   │   ├── store/         # 状态管理
│   │   └── main.ts        # 主应用入口
│   └── index.html         # HTML模板
├── start_backend.py       # 后端启动脚本
├── start_frontend.ps1     # 前端启动脚本（PowerShell）
├── start_frontend.bat     # 前端启动脚本（CMD）
├── start_all.ps1          # 完整启动脚本
├── LEDGER_MODULE_README.md # 账本模块技术文档
└── USAGE_GUIDE.md         # 用户使用指南
```

## 🎨 设计特色

### 配色方案
- **主色调**: `#FFA939` (活力橙) - 用于主要按钮和强调
- **辅助色**: `#70CDE5` (清新蓝) - 用于标签和状态标识
- **背景色**: `#F9F3EE` (温暖米) - 用于页面背景
- **强调色**: `#009CC6` (专业蓝) - 预留扩展使用

### 用户体验
- 📱 完全响应式设计
- ✨ 平滑的动画效果
- 🎯 直观的操作界面
- 🔄 实时数据更新

## 🔐 安全特性

- **密码哈希**: 使用bcrypt加密存储
- **权限控制**: 基于角色的访问控制
- **输入验证**: 前后端双重验证
- **XSS防护**: 内容安全策略

## 📝 使用流程

### 1. 注册登录
1. 访问首页
2. 点击"注册"创建账户
3. 使用注册的邮箱和密码登录

### 2. 创建账本
1. 登录后点击"账本管理"
2. 点击"创建账本"
3. 输入账本名称
4. （可选）关联旅行计划

### 3. 邀请成员
1. 进入账本详情页
2. 点击"添加成员"
3. 输入成员邮箱

### 4. 添加账单
1. 在账本详情页点击"添加账单"
2. 选择账单类型和金额
3. 选择付款人和参与者
4. 保存账单

## 🚧 开发指南

### 开发环境搭建

1. **克隆项目**:
```bash
git clone <repository-url>
cd CoTrip
```

2. **安装后端依赖**:
```bash
cd backend
pip install -r requirements.txt
```

3. **安装前端依赖**:
```bash
cd frontend
npm install
```

### 开发流程

1. **启动开发服务器**（后端）:
```bash
cd backend
python main.py
```

2. **启动开发服务器**（前端）:
```bash
cd frontend
npm run dev
```

3. **代码规范**:
- 使用TypeScript编写前端代码
- 遵循Vue 3 Composition API
- 使用ESLint进行代码检查

## 📊 数据库设计

### 主要数据表

- **users**: 用户信息表
- **ledgers**: 账本信息表
- **bill_items**: 账单条目表
- **user_ledger**: 用户-账本关联表
- **user_billitem**: 用户-账单关联表

### 数据关系

- **用户 ↔ 账本**: 多对多关系
- **用户 ↔ 账单**: 多对多关系
- **账本 ↔ 账单**: 一对多关系

## 🔌 API接口

### 用户接口
- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `PUT /api/users/update-username` - 更新用户名
- `PUT /api/users/update-password` - 更新密码

### 账本接口
- `POST /api/ledgers/` - 创建账本
- `GET /api/ledgers/my-ledgers` - 获取我的账本
- `GET /api/ledgers/{id}` - 获取账本详情
- `PUT /api/ledgers/{id}` - 更新账本
- `DELETE /api/ledgers/{id}` - 删除账本
- `POST /api/ledgers/{id}/members` - 添加成员
- `DELETE /api/ledgers/{id}/members/{user_id}` - 移除成员

### 账单接口
- `POST /api/ledgers/{ledger_id}/bill-items` - 创建账单
- `PUT /api/ledgers/bill-items/{id}` - 更新账单
- `DELETE /api/ledgers/bill-items/{id}` - 删除账单

## 💬 社区支持

### 问题反馈
- **Issue**: 在GitHub仓库提交Issue
- **讨论**: 参与项目讨论
- **文档**: 查看项目文档

### 贡献指南
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

MIT License

## 🤝 团队

- **开发团队**: CoTrip Team
- **贡献者**: 所有为项目做出贡献的开发者

## 📞 联系方式

- **项目主页**: [GitHub Repository]
- **文档地址**: [Project Documentation]
- **技术支持**: [Support Channel]

---

**版本**: 1.0.0
**发布日期**: 2024
**© 2024 CoTrip Team**
