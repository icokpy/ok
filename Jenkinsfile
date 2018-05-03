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

                                   if ( env.BRANCH_NAME == 'master' ) {
                                        dockerTag = "icokpy-${env.BUILD_NUMBER}"
                                   } else {
                                        dockerTag = "${env.BUILD_TAG}".toLowerCase().replaceAll("[^\\p{IsAlphabetic}^\\p{IsDigit}]", "-")
                                   }

                                   def okImage = docker.build("${dockerTag}")

                                   okImage.inside() {
                                        sh 'py.test tests/ --ignore=tests/test_job.py'
                                   }                          

                                   if ( env.BRANCH_NAME == 'master' ) {

                                        docker.withRegistry('https://icokpy.azurecr.io', 'icokpy-registry-credentials') {
                                             okImage = docker.image("icokpy-${env.BUILD_NUMBER}")
                                             okImage.push()
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
                              sh 'py.test tests/ --ignore=tests/test_job.py'
                              sh 'py.test --cov-report term-missing --cov=server tests/  --ignore tests/test_web.py --timeout=30'
                         }
                    }
               }
          }
     }
}
