pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'subscription_service:latest'
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
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
                sshagent(['vps_ssh_credentials']) {
                    sh "ssh user@your_vps_ip docker pull ${env.DOCKER_IMAGE}"
                    sh "ssh user@your_vps_ip docker-compose -f /path/to/your/docker-compose.yml up -d"
                }
            }
        }
    }
}
