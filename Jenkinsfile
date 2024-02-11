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
                    // Build the Docker image with the tag specified in DOCKER_IMAGE environment variable
                    sh "docker build -t ${env.DOCKER_IMAGE} ."
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Login to Docker Hub using credentials stored in Jenkins
                    withCredentials([usernamePassword(credentialsId: 'ard-dockerhub', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                        sh "echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin"
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Push the image to Docker Hub
                    sh "docker push ${env.DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy to VPS') {
            steps {
                script {
                    // Securely transfer the environment file and deploy using Docker Compose on the VPS
                    withCredentials([file(credentialsId: 'env-file-id', variable: 'ENV_FILE')]) {
                        sshagent(['vps_ssh_credentials']) {
                            sh "scp $ENV_FILE user@your_vps_ip:/path/to/your/.env"
                            sh "ssh user@your_vps_ip 'docker pull ${env.DOCKER_IMAGE}'"
                            sh "ssh user@your_vps_ip 'docker-compose -f /path/to/your/docker-compose.yml up -d'"
                        }
                    }
                }
            }
        }
    }
}
