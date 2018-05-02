/* Jenkinsfile for the IC OKPy fork
 
   Jenkins instance at: http://ok-jenkins.uksouth.cloudapp.azure.com/ 
*/

String dockerTag = "${env.BUILD_TAG}".toLowerCase()

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
                         // Build from default dockerfile
                         agent { 
                              dockerfile { 
                                   label 'linux'
                                   additionalBuildArgs "-t ${dockerTag}"
                              }
                         }    
                         steps { 
                              sh 'py.test tests/ --ignore=tests/test_job.py'
                         }
                    }
                    stage('OK native on Quantal') {
                         // Original OK uses trusty; Azure uses Quantal
                         agent { 
                              label 'linux' 
                         }
                         steps {
                              sh 'sudo apt-get update'
                              // Required for pip and later installs
                              sh 'sudo apt-get -y install curl patch python3'
                              // Ubuntu pip package gives version problems
                              //  with system python-six being too old
                              sh 'curl https://bootstrap.pypa.io/get-pip.py | sudo python3'
                              sh 'sudo pip install -r requirements.txt'
                              sh 'sudo pip install pytest-timeout python-coveralls'
                              sh 'py.test tests/ --ignore=tests/test_job.py'
                              sh 'py.test --cov-report term-missing --cov=server tests/  --ignore tests/test_web.py --timeout=30'
                         }
                     }
               }
          }
     }
     post {  
          success {  
               script {
                    if ( env.BRANCH_NAME == 'master' ) {
                         docker.withRegistry('https://icokpy.azurecr.io', 'icokpy-registry-credentials') {
                          def deployImage = docker.image("${dockerTag}")
                              deployImage.push("deployment:${dockerTag}")
                              deployImage.push('deployment:latest')
                         }
                    }
               }
          }
     }
 
}
