# Deploy to Azure PaaS

These templates deploy Ok.py to Azure. 

## Architecture


## Accept SendGrid Terms

Using PowerShell:

''' Get-AzureRmMarketplaceTerms -Publisher "sendgrid" -Product "sendgrid_azure" -Name "free" | Set-AzureRmMarketplaceTerms -Accept '''

Can be run in the cloud shell.



## ACI 
az container create -g tmpOK --name okaci7 --image marrobi/ok:latest --cpu 2 --memory 3 --port 5000  --ip-address Public -e DATABASE_URL="mysql://adminmarcus%40tmpmrsql:Password1234@tmpmrsql.mysql.database.azure.com:3306/ok" REDIS_HOST="tmpmrredis.redis.cache.windows.net" REDIS_PASSWORD="K8jJnnD4N8TTEkrkyQKo3lZlIa33ol0MGOqK81x4K/Y=" OK_ENV="prod"