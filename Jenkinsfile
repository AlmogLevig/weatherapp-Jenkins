pipeline{

    agent{ label 'testAgent' }

    environment{ docker_id=credentials('deploy_image') }

    stages{

        stage('Build') {
            steps {
                sh "sudo docker build -t ${env.DOCKERHUB_USER}/${env.IMG_NAME}:${env.IMG_TAG} ."
                echo '---This is a Build step---'
            }
        }
        
        stage('run') {
            steps {
                sh "sudo docker container run --name ${env.CON_NAME} -dit -p 80:5000 ${env.DOCKERHUB_USER}/${env.IMG_NAME}:${env.IMG_TAG}"
                echo '---This is a run step---'
            }
        }
        
        stage('delivery image to DockerHub') {
            steps {
                sh 'echo $docker_id_PSW | sudo docker login -u $docker_id_USR --password-stdin'
                sh "sudo docker push ${env.DOCKERHUB_USER}/${env.IMG_NAME}:${env.IMG_TAG}"
                echo '---This is a Artifacts Delivery step---'    
            }
        }
    }
}

    post{

        failure{
            mail to: ${env.MAIL},
            subject: "jenkins build:${currentBuild.currentResult}: ${env.JOB_NAME}",
            body: "OPS! /n something Wrong in your Pipeline${currentBuild.currentResult}: Job ${env.JOB_NAME}\nMore Info can be found here: ${env.BUILD_URL}"
            sh "sudo docker stop ${env.CON_NAME}" 
            sh 'sudo docker system prune -f'
        }

        success{
            mail to: ${env.MAIL},
            subject: "jenkins build:${currentBuild.currentResult}: ${env.JOB_NAME}",
            body: " WOW!!! Youre Amazing Make me a child!${currentBuild.currentResult}: Job ${env.JOB_NAME}\nMore Info can be found here: ${env.BUILD_URL}"
        }
    }