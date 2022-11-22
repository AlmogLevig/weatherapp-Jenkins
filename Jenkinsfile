pipeline{
    agent { label 'testAgent' }

    environment{
        docker_id=credentials('deploy_image')
        // REPO='imageweatherapp/'
        REPO='almoglevig'
        IMG_NAME='webapp_img'
        CON_NAME='webapp_con'
        IMG_TAG="v1.${BUILD_NUMBER}"
        // ARTIFACT_DIR='/imageweatherapp'     
    }

    stages{
        stage('clean'){
            steps {
                sh 'sudo chmod 666 /var/run/docker.sock'
                echo '---This is a clean step---'
            }
        }

        stage('Build') {
            steps {
                sh "sudo docker build -t ${env.REPO}/${env.IMG_NAME}:${env.IMG_TAG} ."
                echo '---This is a Build step---'
            }
        }
        
        stage('run') {
            steps {
                sh "sudo docker container run --name ${env.CON_NAME} -dit -p 80:5000 ${env.REPO}/${env.IMG_NAME}:${env.IMG_TAG}"
                echo '---This is a run step---'
            }
        }

        stage('test & yml configuration'){
            parallel{
            
                stage('test') {
                    steps {
                        sh 'sudo docker exec  webapp_con python3 unit_test.py'             
                        echo '---This is a test step---'  
                    }
                }
            
                stage('yml configuration') {
                    steps {
                        sh "sed -i -e 's/${env.IMG_NAME}.*/${env.IMG_NAME}:${env.IMG_TAG}/' ./deployment.yml"
                        echo '---This is a yml configuration step---'
                    }
                }
            
            }
        }
        
        stage('delivery image to DockerHub') {
            steps {
                sh 'echo $docker_id_PSW | sudo docker login -u $docker_id_USR --password-stdin'
                sh "sudo docker push ${env.REPO}/${env.IMG_NAME}:${env.IMG_TAG}"
                echo '---This is a Artifacts Delivery step---'    
            }
        }
    }

    post{
        
        failure{
            mail to: "almog.levig@gmail.com",
            subject: "jenkins build:${currentBuild.currentResult}: ${env.JOB_NAME}",
            body: "OPS! /n something Wrong in your Pipeline${currentBuild.currentResult}: Job ${env.JOB_NAME}\nMore Info can be found here: ${env.BUILD_URL}"
            sh "sudo docker stop ${env.CON_NAME}" 
            sh 'sudo docker system prune -f'
        }

        success{
            mail to: "almog.levig@gmail.com",
            subject: "jenkins build:${currentBuild.currentResult}: ${env.JOB_NAME}",
            body: " WOW!!! ${currentBuild.currentResult}: Job ${env.JOB_NAME}\nMore Info can be found here: ${env.BUILD_URL}"
        }
    }
}

        // stage('deployment') {
        //     steps{
        //         sshagent(['f8491a07-2b62-4e1d-90bb-dda23355138a']) {
        //             sh '''
        //                 scp deployment.yml script.sh ubuntu@ip-172-31-30-238.ec2.internal:"~"
        //                 ssh -t ubuntu@ip-172-31-30-238.ec2.internal 'chmod +x script.sh | sh script.sh' 
        //                 ssh -t ubuntu@ip-172-31-30-238.ec2.internal 'kubectl apply -f deployment.yml'
        //                 ssh -t ubuntu@ip-172-31-30-238.ec2.internal 'kubectl port-forward service/weathapp-ser --address 0.0.0.0 5000:5000'
        //                 '''
        //         }
        //     }
        // }

        // stage('delivery artifact') {
        //     steps {
        //         rtDockerPush(
        //             serverId: 'calc_artifacts',
        //             image:  "${env.ARTIFACT_DIR}/${env.IMG_NAME}:${env.IMG_TAG}",
        //             targetRepo:"${env.REPO}"
        //         )
        //         echo '---This is a Artifacts Delivery step---'    
            // }
        // }
        // stage('deployment') {
        //     steps{
        //         sshagent(['f8491a07-2b62-4e1d-90bb-dda23355138a']) {
        //             sh '''
        //                 scp deployment.yml script.sh ubuntu@ip-172-31-30-238.ec2.internal:"~"
        //                 ssh -t ubuntu@ip-172-31-30-238.ec2.internal 
        //                     'chmod +x script.sh | ./script.sh' 
        //                 ssh -t ubuntu@ip-172-31-30-238.ec2.internal
        //                     'kubectl create -f ./deployment.yml | kubectl port-forword service/weather_app_ser 5000:5000'
        //                 '''
        //         }
        //     }
        // }