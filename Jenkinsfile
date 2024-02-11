pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'subscription_service:latest'
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Assuming your Dockerfile doesn't require env vars to build. 
                    // If it does, consider using --build-arg KEY=VALUE here.
                    docker.build(env.DOCKER_IMAGE)
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Add docker login if needed
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub_credentials') {
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
