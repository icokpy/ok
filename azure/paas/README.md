# Deploy to Azure PaaS

These templates deploy Ok.py to Azure. In a production environment you may wish to customize these templates to share resources between environments and to adjust resource sizing. For example you may wish to use a single mySQL server with multiple databases, rather than one server per environment.
<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Ficokpy%2Fok%2Fmaster%2Fazure%2Fpaas%2Fazure.deploy.json" target="_blank">
    <img src="http://azuredeploy.net/deploybutton.png"/>
</a>

## Architecture

![Azure PaaS Architecture](./img/arch.PNG)


## Accept SendGrid Terms
Prior to deploying the tempkate 
Using PowerShell:

''' Get-AzureRmMarketplaceTerms -Publisher "sendgrid" -Product "sendgrid_azure" -Name "free" | Set-AzureRmMarketplaceTerms -Accept '''

This can be run in the cloud shell.



