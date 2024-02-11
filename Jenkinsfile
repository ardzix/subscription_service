pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'ardzix/subscription_service:latest'
    }
    stages {
                
        stage('Build Docker Image') {
            steps {
                script {
                    // Print the current working directory for debugging
                    sh 'pwd'
                    // Assuming Dockerfile is in the root of the checked-out repo
                    sh 'docker build -t subscription_service:latest .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Add docker login if needed
                    docker.withRegistry('https://registry.hub.docker.com', 'ard-dockerhub') {
                        docker.image(env.DOCKER_IMAGE).push()
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
