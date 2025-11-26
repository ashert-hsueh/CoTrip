@echo off
chcp 65001 >nul
title CoTrip Frontend Server

echo 🌟 CoTrip 前端服务启动器
echo ========================
echo.

REM 检查Node.js是否安装
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Node.js，请先安装Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js版本:
node --version
echo.

REM 检查npm是否安装
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到npm，请先安装npm
    pause
    exit /b 1
)

echo ✅ npm版本:
npm --version
echo.

REM 进入frontend目录
cd frontend

REM 检查是否已安装依赖
if not exist "node_modules" (
    echo 📦 安装前端依赖包...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装成功
    echo.
)

echo 🚀 启动CoTrip前端服务...
echo 📡 服务地址: http://localhost:5173
echo 🔄 按 Ctrl+C 停止服务
echo.

REM 启动开发服务器
npm run dev

if %errorlevel% neq 0 (
    echo.
    echo ❌ 启动失败，请检查错误信息
    pause
    exit /b 1
)
