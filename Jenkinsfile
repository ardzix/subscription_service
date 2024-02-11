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
                    withCredentials([file(credentialsId: 'subscription-service-env', variable: 'ENV_FILE')]) {
                        sshagent(['stag-arnatech-sa-01']) {

                            sh 'ls -lah' // Lists the current directory contents
                            echo "ENV_FILE path: $ENV_FILE" // Echoes the ENV_FILE variable to confirm its value

                            sh "scp -o StrictHostKeyChecking=no $ENV_FILE root@172.105.124.43:subscription_service/.env"
                            sh "ssh -o StrictHostKeyChecking=no root@172.105.124.43 'docker pull ${env.DOCKER_IMAGE}'"
                            sh "ssh -o StrictHostKeyChecking=no root@172.105.124.43 'docker run -d -p 8001:8001 --restart always --network development --name subscription-service ${env.DOCKER_IMAGE}'"

                        }
                    }
                }
            }
        }
    }
           
}