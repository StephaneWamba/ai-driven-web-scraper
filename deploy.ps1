# AI-Driven E-Commerce Intelligence Scraper - Deployment Script
# This script deploys the infrastructure using Terraform

param(
    [string]$Environment = "portfolio",
    [string]$AWSRegion = "us-east-1",
    [string]$DBPassword
)

Write-Host "🚀 AI-Driven E-Commerce Intelligence Scraper - Deployment Script" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green

# Check if Terraform is installed
try {
    $terraformVersion = terraform version
    Write-Host "✅ Terraform found: $($terraformVersion.Split("`n")[0])" -ForegroundColor Green
}
catch {
    Write-Host "❌ Terraform not found. Please install Terraform first." -ForegroundColor Red
    exit 1
}

# Check if AWS CLI is configured
try {
    $awsIdentity = aws sts get-caller-identity
    Write-Host "✅ AWS CLI configured" -ForegroundColor Green
}
catch {
    Write-Host "❌ AWS CLI not configured. Please run 'aws configure' first." -ForegroundColor Red
    exit 1
}

# Validate required parameters
if (-not $DBPassword) {
    Write-Host "❌ Database password is required. Use -DBPassword parameter." -ForegroundColor Red
    Write-Host "Example: .\deploy.ps1 -DBPassword 'your_secure_password'" -ForegroundColor Yellow
    exit 1
}

# Navigate to terraform directory
Set-Location terraform

Write-Host "`n📋 Deployment Configuration:" -ForegroundColor Cyan
Write-Host "   Environment: $Environment" -ForegroundColor White
Write-Host "   AWS Region: $AWSRegion" -ForegroundColor White
Write-Host "   Database Password: [HIDDEN]" -ForegroundColor White

# Confirm deployment
$confirm = Read-Host "`nDo you want to proceed with deployment? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host "`n🔧 Initializing Terraform..." -ForegroundColor Cyan
try {
    terraform init
    if ($LASTEXITCODE -ne 0) {
        throw "Terraform init failed"
    }
}
catch {
    Write-Host "❌ Terraform initialization failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n📊 Planning Terraform deployment..." -ForegroundColor Cyan
try {
    terraform plan -var="environment=$Environment" -var="aws_region=$AWSRegion" -var="db_password=$DBPassword" -out=tfplan
    if ($LASTEXITCODE -ne 0) {
        throw "Terraform plan failed"
    }
}
catch {
    Write-Host "❌ Terraform planning failed: $_" -ForegroundColor Red
    exit 1
}

# Show plan summary
Write-Host "`n📋 Deployment Plan Summary:" -ForegroundColor Cyan
terraform show tfplan | Select-String -Pattern "Plan:" -Context 0, 10

# Final confirmation
$confirm = Read-Host "`nDo you want to apply this plan? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host "`n🚀 Applying Terraform configuration..." -ForegroundColor Cyan
try {
    terraform apply tfplan
    if ($LASTEXITCODE -ne 0) {
        throw "Terraform apply failed"
    }
}
catch {
    Write-Host "❌ Terraform deployment failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Deployment completed successfully!" -ForegroundColor Green

# Show outputs
Write-Host "`n📊 Deployment Outputs:" -ForegroundColor Cyan
terraform output

Write-Host "`n🔗 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Access the server via AWS Systems Manager Session Manager" -ForegroundColor White
Write-Host "2. Check application status: curl http://[SERVER_IP]:8000/health" -ForegroundColor White
Write-Host "3. View API docs: http://[SERVER_IP]:8000/docs" -ForegroundColor White

Write-Host "`n💡 Tips:" -ForegroundColor Yellow
Write-Host "- The application will take a few minutes to fully start up" -ForegroundColor White
Write-Host "- Check the logs: sudo journalctl -u ai-scraper -f" -ForegroundColor White
Write-Host "- To destroy infrastructure: terraform destroy" -ForegroundColor White

# Return to original directory
Set-Location ..

Write-Host "`n🎉 Deployment script completed!" -ForegroundColor Green 