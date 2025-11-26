<#
.SYNOPSIS
CoTrip完整服务启动脚本 (PowerShell版本)
.DESCRIPTION
同时启动CoTrip的后端和前端服务
#>

Write-Host "🌟 CoTrip 完整服务启动器" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行（可选，但某些情况下需要）
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  建议以管理员身份运行此脚本以获得最佳体验" -ForegroundColor Yellow
    Write-Host ""
}

# 启动后端服务
Write-Host "🚀 启动后端服务..." -ForegroundColor Cyan
$backendScript = Join-Path -Path $PSScriptRoot -ChildPath "start_backend.py"

# 在新窗口中启动后端
Start-Process -FilePath "python" -ArgumentList $backendScript -WindowStyle Normal -WorkingDirectory $PSScriptRoot

# 等待后端启动
Write-Host "⏳ 等待后端服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 启动前端服务
Write-Host "🚀 启动前端服务..." -ForegroundColor Cyan
$frontendScript = Join-Path -Path $PSScriptRoot -ChildPath "start_frontend.ps1"

# 在新窗口中启动前端
Start-Process -FilePath "powershell" -ArgumentList "-ExecutionPolicy Bypass -File `"$frontendScript`"" -WindowStyle Normal -WorkingDirectory $PSScriptRoot

Write-Host ""
Write-Host "✅ 服务启动完成！" -ForegroundColor Green
Write-Host "📡 后端地址: http://localhost:8000" -ForegroundColor Green
Write-Host "🌐 前端地址: http://localhost:5173" -ForegroundColor Green
Write-Host "📖 API文档: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "🔄 按任意键退出..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
