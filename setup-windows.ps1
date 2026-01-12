# setup-windows.ps1 - Complete Windows Setup for DevOps Platform Agent
# Run as Administrator: PowerShell -ExecutionPolicy Bypass -File setup-windows.ps1

Write-Host "=== DevOps Platform Agent - Windows Setup ===" -ForegroundColor Green

# Check Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: Run as Administrator" -ForegroundColor Red
    exit 1
}

# 1. Install Chocolatey
Write-Host "[1/10] Installing Chocolatey..." -ForegroundColor Cyan
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# 2. Install Tools

Write-Host "[3/10] Installing Node.js 18..." -ForegroundColor Cyan
choco install nodejs-lts -y

Write-Host "[4/10] Installing kubectl..." -ForegroundColor Cyan
choco install kubernetes-cli -y

Write-Host "[5/10] Installing Helm..." -ForegroundColor Cyan
choco install kubernetes-helm -y

Write-Host "[6/10] Installing Terraform..." -ForegroundColor Cyan
choco install terraform -y

Write-Host "[7/10] Installing Azure CLI..." -ForegroundColor Cyan
choco install azure-cli -y

Write-Host "[8/10] Installing k9s..." -ForegroundColor Cyan
choco install k9s -y

refreshenv

# 9. Install Python packages
Write-Host "[9/10] Installing Python packages..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install langchain==0.1.20 langgraph==0.0.55 langchain-openai langchain-anthropic langchain-community fastapi uvicorn pydantic sqlalchemy redis kubernetes prometheus-api-client azure-identity PyGithub python-dotenv structlog pytest httpx

# 10. Install Node packages
Write-Host "[10/10] Installing Node packages..." -ForegroundColor Cyan
npm install -g typescript @types/node

Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Enable Kubernetes in Docker Desktop" -ForegroundColor White
Write-Host "2. Run: ollama pull codellama:34b" -ForegroundColor White
Write-Host "3. Run: docker-compose up -d" -ForegroundColor White
