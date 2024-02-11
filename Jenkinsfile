pipeline {
    agent any
    environment {
        // Define the full image name including the registry prefix
        DOCKER_IMAGE = 'ardzix/subscription_service:latest'
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Print the current working directory for debugging
                    sh 'pwd'
                    // Correct the build command to use the full Docker image name
                    sh "docker build -t ${env.DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'ard-dockerhub', passwordVariable: 'DOCKERHUB_PASS', usernameVariable: 'DOCKERHUB_USER')]) {
                        sh "echo $DOCKERHUB_PASS | docker login registry.hub.docker.com -u $DOCKERHUB_USER --password-stdin"
                        sh "docker push ${env.DOCKER_IMAGE}"
                    }
                }
            }
        }


        stage('Deploy to VPS') {
            steps {
                withCredentials([file(credentialsId: 'env-file-id', variable: 'ENV_FILE')]) {
                    sshagent(['vps_ssh_credentials']) {
                        // Assuming your docker-compose or deployment script uses the .env file
                        sh "scp $ENV_FILE user@your_vps_ip:/path/to/your/.env"
                        sh "ssh user@your_vps_ip 'docker pull ${env.DOCKER_IMAGE}'"
                        sh "ssh user@your_vps_ip 'docker-compose -f /path/to/your/docker-compose.yml up -d'"
                    }
                }
            }
        }
    }
}
