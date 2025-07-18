# AI Scraper - Status Checker
# This script checks the deployment status and provides connection information

Write-Host "Checking AI Scraper Infrastructure Status..." -ForegroundColor Cyan

# Navigate to terraform directory
Set-Location terraform

try {
    # Get Terraform outputs
    Write-Host "`nInfrastructure Status:" -ForegroundColor Green
    
    $outputs = terraform output -json | ConvertFrom-Json
    
    if ($outputs.app_public_ip.value) {
        Write-Host "✅ EC2 Instance: $($outputs.app_public_ip.value)" -ForegroundColor Green
        Write-Host "✅ Database: $($outputs.database_endpoint.value)" -ForegroundColor Green
        Write-Host "✅ S3 Bucket: $($outputs.s3_bucket_name.value)" -ForegroundColor Green
        
        Write-Host "`nAccess URLs:" -ForegroundColor Yellow
        Write-Host "   API: http://$($outputs.app_public_ip.value):8000" -ForegroundColor White
        Write-Host "   Docs: http://$($outputs.app_public_ip.value):8000/docs" -ForegroundColor White
        Write-Host "   Health: http://$($outputs.app_public_ip.value):8000/health" -ForegroundColor White
        
        Write-Host "`nTesting API Health..." -ForegroundColor Cyan
        try {
            $response = Invoke-RestMethod -Uri "http://$($outputs.app_public_ip.value):8000/health" -TimeoutSec 10
            Write-Host "✅ API is responding: $($response.status)" -ForegroundColor Green
        }
        catch {
            Write-Host "⏳ API is starting up... (This may take 2-3 minutes)" -ForegroundColor Yellow
        }
        
    }
    else {
        Write-Host "⏳ Infrastructure is still being created..." -ForegroundColor Yellow
        Write-Host "   Run this script again in a few minutes" -ForegroundColor White
    }
    
}
catch {
    Write-Host "❌ Error checking status: $_" -ForegroundColor Red
}

# Return to original directory
Set-Location ..

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Wait for deployment to complete (2-3 minutes)" -ForegroundColor White
Write-Host "2. Run this script again to check status" -ForegroundColor White
Write-Host "3. Test the API endpoints" -ForegroundColor White
Write-Host "4. Begin frontend development" -ForegroundColor White 