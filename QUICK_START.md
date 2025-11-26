# 🚀 CoTrip 快速开始指南

## 一分钟启动教程

### 方法一：一键启动（推荐）

1. **打开PowerShell**
2. **进入项目目录**：
   ```powershell
   cd D:/Repositories/CoTrip
   ```
3. **运行启动脚本**：
   ```powershell
   .\start_all.ps1
   ```

### 方法二：分别启动

**启动后端：**
```powershell
python start_backend.py
```

**启动前端：**
```powershell
.\start_frontend.ps1
```

### 方法三：手动启动

**后端启动：**
```bash
cd backend
pip install fastapi uvicorn sqlalchemy passlib python-multipart
python main.py
```

**前端启动：**
```bash
cd frontend
npm install
npm run dev
```

## 📱 访问地址

启动成功后，在浏览器中打开：

- 🌐 **前端应用**: `http://localhost:5173`
- 📡 **后端API**: `http://localhost:8000`
- 📖 **API文档**: `http://localhost:8000/docs`

## 🎯 首次使用步骤

1. **注册账户**:
   - 打开前端应用
   - 点击"注册"
   - 填写用户名、邮箱和密码

2. **登录系统**:
   - 使用注册的邮箱和密码登录
   - 系统会自动跳转到首页

3. **创建账本**:
   - 点击导航栏"账本管理"
   - 点击"创建账本"按钮
   - 输入账本名称（如："三亚旅行账本"）
   - 点击"创建"

4. **添加账单**:
   - 进入刚创建的账本详情页
   - 点击"添加账单"按钮
   - 填写账单信息：
     - 选择类型（如：餐饮）
     - 输入金额（如：100）
     - 选择付款人
     - 选择参与者
     - 添加备注（可选）
   - 点击"添加账单"

5. **邀请成员**:
   - 在账本详情页点击"添加成员"
   - 输入成员邮箱邀请加入

## 🎨 功能特色

### 账本管理
- ✅ 支持创建多个独立账本
- ✅ 多人实时协同管理
- ✅ 旅行计划关联功能
- ✅ 详细的统计信息

### 账单记录
- ✅ 5种账单类型：住宿、餐饮、交通、门票、其他
- ✅ 精确到分的金额记录
- ✅ 灵活的付款人和参与者选择
- ✅ 时间和备注管理

### 界面设计
- ✨ 现代化的橙色主题
- 📱 完全响应式设计
- 🎯 直观的操作界面
- 🔄 实时数据更新

## 🔧 常见问题

### Q: 端口被占用怎么办？
A: Vite会自动尝试其他端口，如5174、5175等。

### Q: 依赖安装失败？
A: 检查网络连接，或手动安装依赖：
```bash
# 后端
pip install fastapi uvicorn sqlalchemy passlib python-multipart

# 前端
cd frontend
npm install --force
```

### Q: 数据库连接失败？
A: 确保SQLite已正确安装，检查数据库文件路径。

### Q: 如何重置密码？
A: 在用户管理页面可以修改密码。

## 📞 技术支持

### 开发环境要求
- **Python**: 3.8+
- **Node.js**: 16+
- **npm**: 8+

### 联系方式
- 查看 `LEDGER_MODULE_README.md` 获取技术架构说明
- 查看 `USAGE_GUIDE.md` 获取详细使用指南
- 提交Issue到项目仓库

## 🎉 开始使用

现在您已经成功启动了CoTrip！开始创建您的第一个账本，记录美好的旅行时光吧！

**祝您使用愉快！** ✨

---
CoTrip Team | 2024
