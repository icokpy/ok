/* Jenkinsfile for the IC OKPy fork
 
   Jenkins instance at: http://ok-jenkins.uksouth.cloudapp.azure.com/ 
*/

// Run in declarative pipeline
pipeline {
     // Agent will be specified per-stage
     agent none
     // Force testing environment 
     environment { 
         OK_ENV = 'test'
     }
     stages {
          stage('Testing') {
               // Docker and native builds are independent of each other
               parallel {
                    stage('OK docker') {
                         agent { label 'azure-linux' }
                         steps {
                              // docker methods need to drop into scripted pipeline    
                              script {

                                   // generate version, it's important to remove the trailing new line in git describe output
                                   def version = sh script: 'git rev-parse --short HEAD | tr -d "\n"', returnStdout: true
                                   def imageName = "icokpy"
                                   def imageTag = "${env.BUILD_NUMBER}_${version}"
                                   def acrHost = 'icokpy.azurecr.io'
                                   def acrUrl = "https://${acrHost}"
                                   def location = 'westeurope'
                                   def webAppName = 'icokpy'
                                   def webAppResourceGroup = "icokpy-dev-${location}"

                               def okImage = docker.build("${imageName}:${imageTag}")

                                   okImage.inside() {
                                        sh 'py.test tests/ --ignore=tests/test_job.py'
                                   }                          

                                   if ( env.BRANCH_NAME == 'master' ) {
                                        // Push the new image to acr
                                        docker.withRegistry("${acrUrl}", 'icokpy-registry-credentials') {
                                             okImage.push()
                                             okImage.push("latest")
                                        }

                                        // Install azure-cli tools on the build slave
                                        sh 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ xenial main" | sudo tee /etc/apt/sources.list.d/azure-cli.list'
                                        sh 'sudo apt-key adv --keyserver packages.microsoft.com --recv-keys 52E16F86FEE04B979B07E28DB02C46DF417A0893'
                                        sh 'curl -L https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -'
                                        sh 'sudo apt-get -y install apt-transport-https'
                                        sh 'sudo apt-get update && sudo apt-get -y install azure-cli'

                                        // Deploy
                                        withCredentials([azureServicePrincipal('jenkins-service-principal')]) {
                                             sh "az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET -t $AZURE_TENANT_ID"
                                             sh "az account set -s $AZURE_SUBSCRIPTION_ID"
                                             sh "az group create --name ${webAppResourceGroup} --location ${location}"
                                             withCredentials([usernamePassword(credentialsId: 'icokpy-mysql-credentials', usernameVariable: 'mysqlUser', passwordVariable: 'mysqlPass')]) {
                                               withCredentials([usernamePassword(credentialsId: 'icokpy-sendgrid', usernameVariable: 'sendgridUser', passwordVariable: 'sendgridPass')]) {
                                                 withCredentials([usernamePassword(credentialsId: 'icokpy-registry-credentials', usernameVariable: 'acrUser', passwordVariable: 'acrPass')]) {
                                                   withCredentials([usernamePassword(credentialsId: 'icokpy-azure-app-id', usernameVariable: 'azureAdAppID', passwordVariable: 'azureAdAppSecret')]) {
                                                     // Horrible hack - the first deployment will fail with resources not yet available. so we need to ignore
                                                     // the error exit state and force clean exit with '|| true'
                                                     sh """
                                                       az group deployment create --resource-group ${webAppResourceGroup} --template-file azure/paas/azure.deploy.json \
                                                         --parameters @azure/paas/azure.deploy.parameters.json --parameters dockerImageName=${imageName}:${imageTag} \
                                                         --parameters mySqlUsername=${mysqlUser} --parameters mySqlAdminPassword=${mysqlPass} \
                                                         --parameters sendgridPassword=${sendgridPass} \
                                                         --parameters dockerRegistryUsername=${acrUser} --parameters dockerRegistryPassword=${acrPass} \
                                                         --parameters dockerRegistryUrl=${acrHost} --parameter uniqueAppName='icokpy-dev' --parameter OkPyEnvironment='dev' \
                                                         --parameters templateBaseURL=https://raw.githubusercontent.com/icokpy/ok/master/azure/paas/ \
                                                         --parameters azureAdAppID=${azureAdAppID} --parameters azureAdAppSecret=${azureAdAppSecret} \
                                                         --parameters azureAdTenantID='ImperialLondon.onmicrosoft.com' || true
                                                       az group deployment create --resource-group ${webAppResourceGroup} --template-file azure/paas/azure.deploy.json \
                                                         --parameters @azure/paas/azure.deploy.parameters.json --parameters dockerImageName=${imageName}:${imageTag} \
                                                         --parameters mySqlUsername=${mysqlUser} --parameters mySqlAdminPassword=${mysqlPass} \
                                                         --parameters sendgridPassword=${sendgridPass} \
                                                         --parameters dockerRegistryUsername=${acrUser} --parameters dockerRegistryPassword=${acrPass} \
                                                         --parameters dockerRegistryUrl=${acrHost} --parameter uniqueAppName='icokpy-dev' --parameter OkPyEnvironment='dev' \
                                                         --parameters templateBaseURL=https://raw.githubusercontent.com/icokpy/ok/master/azure/paas/ \
                                                         --parameters azureAdAppID=${azureAdAppID} --parameters azureAdAppSecret=${azureAdAppSecret} \
                                                         --parameters azureAdTenantID='ImperialLondon.onmicrosoft.com'
                                                       """
                                                   }
                                                 }
                                               }
                                             }
                                             sh 'az logout'
                                        }
                                   }
                              }
                         }
                    }

                    stage('OK native') {
                         agent { label 'azure-linux' }
                         steps {
                              sh 'sudo apt-get update'
                              // Required for pip and later installs
                              sh 'sudo apt-get -y install curl patch python3'
                              // Ubuntu pip package gives version problems
                              //  with system python-six being too old
                              sh 'curl https://bootstrap.pypa.io/get-pip.py | sudo python3'
                              sh 'sudo pip install -r requirements.txt'
                              sh 'sudo pip install pytest-timeout python-coveralls'
                              sh 'py.test --cov-report term-missing --cov=server tests/  --ignore tests/test_web.py --timeout=30'
                         }
                    }
               }
          }
     }
}
