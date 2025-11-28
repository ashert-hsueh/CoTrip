# 账本和账单模块说明

## 📋 功能概述

CoTrip项目新增的账本和账单模块允许用户：

### 账本功能
- ✅ 创建和管理多个账本
- ✅ 邀请成员共同管理账本
- ✅ 关联到旅行计划
- ✅ 账本成员权限管理
- ✅ 查看账本统计信息（总支出、成员数量、账单数量）

### 账单功能
- ✅ 添加不同类型的账单（住宿、餐饮、交通、门票、其他）
- ✅ 记录金额、付款人、参与者
- ✅ 添加备注信息
- ✅ 按时间和类型筛选账单
- ✅ 编辑和删除账单

### 技术特性
- 🔐 基于JWT的用户认证
- 🎨 响应式设计，适配移动端和桌面端
- 💾 SQLite数据库持久化
- 🔄 实时数据同步
- 🎯 权限控制（只有成员可操作）

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装Python后端依赖
cd backend
pip install -r requirements.txt  # 如果没有requirements.txt则手动安装所需包

# 安装Node.js前端依赖
cd ../frontend
npm install
```

### 2. 启动后端服务

```bash
cd backend
python main.py
```

后端服务将在 `http://localhost:8000` 启动。

### 3. 启动前端服务

```bash
cd frontend
npm run dev
```

前端应用将在 `http://localhost:5173` 启动。

### 4. 访问应用

在浏览器中访问 `http://localhost:5173`，点击"账本管理"即可开始使用。

## 🏗️ 技术架构

### 后端架构（四层结构）

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Presentation   │────▶│  Application    │────▶│  Persistence    │────▶│  Database       │
│  Layer          │     │  Layer          │     │  Layer          │     │  Layer          │
│  (API Routes)   │     │  (Business      │     │  (Data          │     │  (SQLAlchemy    │
│                 │     │   Logic)        │     │   Access)       │     │   ORM)          │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### 主要文件说明

**数据库层 (Database Layer)**
- `backend/database/entities/ledger_entity.py` - 账本和账单的SQLAlchemy实体定义
- `backend/database/__init__.py` - 数据库连接和表创建

**持久化层 (Persistence Layer)**
- `backend/persistence/ledger_repository.py` - 账本和账单的数据访问操作

**应用层 (Application Layer)**
- `backend/application/ledger_service.py` - 业务逻辑处理
- `backend/application/models/ledger.py` - 请求响应模型定义

**表示层 (Presentation Layer)**
- `backend/presentation/ledger_routes.py` - API端点定义
- `backend/main.py` - 主应用入口

### 前端架构

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Components     │────▶│  Pages          │────▶│  API Clients    │
│  (Vue Components│     │  (Page Views)   │     │  (HTTP Requests)|
│  like BillModal)│     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### 主要文件说明

**页面组件**
- `frontend/src/pages/LedgerListPage.vue` - 账本列表页面
- `frontend/src/pages/LedgerDetailPage.vue` - 账本详情页面

**功能组件**
- `frontend/src/components/BillItemModal.vue` - 账单弹窗组件

**API客户端**
- `frontend/src/api/ledger.ts` - 账本和账单的API请求封装

**路由配置**
- `frontend/src/router/index.ts` - Vue Router配置

## 🗄️ 数据库设计

### 主要数据表

1. **ledgers (账本表)**
   - `id` - 主键
   - `title` - 账本名称
   - `creator_id` - 创建者ID（外键关联users表）
   - `travel_plan_id` - 旅行计划ID（可选）
   - `created_at` - 创建时间
   - `updated_at` - 更新时间

2. **bill_items (账单条目表)**
   - `id` - 主键
   - `ledger_id` - 所属账本ID（外键关联ledgers表）
   - `type` - 账单类型（hotel, meal, transport, ticket, other）
   - `amount` - 金额（分）
   - `payer_id` - 付款人ID（外键关联users表）
   - `description` - 备注（可选）
   - `occurred_at` - 发生时间

3. **user_ledger (用户-账本关联表)**
   - `user_id` - 用户ID（外键关联users表）
   - `ledger_id` - 账本ID（外键关联ledgers表）
   - 复合主键

4. **user_billitem (用户-账单关联表)**
   - `user_id` - 用户ID（外键关联users表）
   - `billitem_id` - 账单ID（外键关联bill_items表）
   - 复合主键

## 🔌 API接口

### 账本相关接口

- `POST /api/ledgers/` - 创建账本
- `GET /api/ledgers/my-ledgers` - 获取当前用户的所有账本
- `GET /api/ledgers/{ledger_id}` - 获取账本详情
- `PUT /api/ledgers/{ledger_id}` - 更新账本信息
- `DELETE /api/ledgers/{ledger_id}` - 删除账本
- `POST /api/ledgers/{ledger_id}/members` - 添加成员
- `DELETE /api/ledgers/{ledger_id}/members/{user_id}` - 移除成员

### 账单相关接口

- `POST /api/ledgers/{ledger_id}/bill-items` - 创建账单
- `PUT /api/ledgers/bill-items/{bill_item_id}` - 更新账单
- `DELETE /api/ledgers/bill-items/{bill_item_id}` - 删除账单

## 🎨 设计规范

### 配色方案
- **主色调**: `#FFA939` (橙色) - 用于主要按钮和强调
- **辅助色**: `#70CDE5` (蓝色) - 用于标签和状态标识
- **背景色**: `#F9F3EE` (浅米色) - 用于页面背景
- **强调色**: `#009CC6` (深蓝色) - 预留扩展使用

### 交互设计
- ✨ 平滑的过渡动画
- 📱 响应式布局适配
- 🔄 实时数据更新
- 🎯 清晰的视觉反馈

## 🔐 权限控制

### 账本权限
- ✅ 账本创建者可以删除账本和管理成员
- ✅ 所有成员可以查看账本详情和账单
- ✅ 所有成员可以添加、编辑和删除账单

### 账单权限
- ✅ 只有账本成员可以操作账单
- ✅ 付款人和参与者必须是账本成员

## 📝 使用流程

### 1. 创建账本
1. 点击"创建账本"按钮
2. 输入账本名称
3. （可选）关联旅行计划
4. 完成创建

### 2. 管理成员
1. 进入账本详情页
2. 点击"添加成员"
3. 输入成员邮箱邀请加入

### 3. 添加账单
1. 进入账本详情页
2. 点击"添加账单"
3. 选择账单类型
4. 输入金额和其他信息
5. 选择付款人和参与者
6. 保存账单

### 4. 查看统计
- 在账本列表页查看所有账本概览
- 在账本详情页查看详细统计信息
- 使用筛选功能查看特定类型账单

## 🚧 注意事项

### 当前限制
1. **用户搜索**: 添加成员时需要手动输入用户ID（需要实现用户搜索API）
2. **JWT认证**: 当前使用固定用户ID，生产环境需要实现完整的JWT认证
3. **旅行计划关联**: 需要实现旅行计划模块的API
4. **前端样式**: 部分图标和样式需要根据实际资源调整

### 扩展建议
1. 🔄 实现实时协作功能
2. 📊 添加图表统计分析
3. 💬 集成聊天功能
4. 📤 导出账单数据
5. 💰 实现自动结算功能

## 🐛 常见问题

### Q: 如何修改账本名称？
A: 在账本详情页点击账本名称旁边的"编辑名称"按钮即可修改。

### Q: 如何删除账本？
A: 只有账本创建者可以在账本列表页点击删除按钮删除账本。

### Q: 如何添加成员？
A: 在账本详情页点击"添加成员"按钮，输入成员邮箱即可邀请。

### Q: 如何处理账单纠纷？
A: 建议通过沟通解决，系统支持修改和删除账单。

## 📞 技术支持

如有问题或建议，请提交Issue或联系开发团队。

---

**版本**: 1.0.0
**最后更新**: 2024
**开发团队**: CoTrip Team
