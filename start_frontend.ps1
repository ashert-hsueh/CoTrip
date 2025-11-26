<#
.SYNOPSIS
CoTrip前端服务启动脚本 (PowerShell版本)
.DESCRIPTION
用于在Windows PowerShell中启动CoTrip前端开发服务器
#>

Write-Host "🌟 CoTrip 前端服务启动器" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# 检查Node.js是否安装
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js版本: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Node.js，请先安装Node.js" -ForegroundColor Red
    Write-Host "下载地址: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "按回车键退出..."
    exit 1
}

Write-Host ""

# 检查npm是否安装
try {
    $npmVersion = npm --version
    Write-Host "✅ npm版本: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到npm，请先安装npm" -ForegroundColor Red
    Read-Host "按回车键退出..."
    exit 1
}

Write-Host ""

# 进入frontend目录
$frontendPath = Join-Path -Path $PSScriptRoot -ChildPath "frontend"
Set-Location -Path $frontendPath

# 检查是否已安装依赖
$nodeModulesPath = Join-Path -Path $frontendPath -ChildPath "node_modules"
if (-not (Test-Path -Path $nodeModulesPath)) {
    Write-Host "📦 安装前端依赖包..." -ForegroundColor Yellow
    try {
        npm install
        Write-Host "✅ 依赖安装成功" -ForegroundColor Green
    } catch {
        Write-Host "❌ 依赖安装失败: $_" -ForegroundColor Red
        Read-Host "按回车键退出..."
        exit 1
    }
    Write-Host ""
}

Write-Host "🚀 启动CoTrip前端服务..." -ForegroundColor Cyan
Write-Host "📡 服务地址: http://localhost:5173" -ForegroundColor Green
Write-Host "🔄 按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动开发服务器
try {
    npm run dev
} catch {
    Write-Host ""
    Write-Host "❌ 启动失败，请检查错误信息: $_" -ForegroundColor Red
    Read-Host "按回车键退出..."
    exit 1
}
