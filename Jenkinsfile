pipeline {
    agent any
    environment {
        DOCKER_IMAGE_NAME_CLIENT = 'hariharan1112/chat-client'
        DOCKER_IMAGE_NAME_SERVER = 'hariharan1112/chat-server'
    }
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Clean up old images
                    sh 'rm -rf ChatApp'
                    // Clone the repository
                    sh 'git clone https://github.com/HARIHARANJAYARAJ/hii.git'
                    dir('ChatApp') {
                        // Build Docker images
                        sh '''
                            docker build -t $DOCKER_IMAGE_NAME_CLIENT ./client
                            docker build -t $DOCKER_IMAGE_NAME_SERVER ./server
                        '''
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                 usernameVariable: 'DOCKERHUB_USER',
                                                 passwordVariable: 'DOCKERHUB_PASS')]) {
                    script {
                        // Log in to Docker Hub
                        sh '''
                            echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                            docker push $DOCKER_IMAGE_NAME_CLIENT:latest
                            docker push $DOCKER_IMAGE_NAME_SERVER:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                script {
                    // Deploy the Docker containers (example using Docker Compose or kubectl)
                    sh '''
                        docker run -d --name chat-client -p 80:80 $DOCKER_IMAGE_NAME_CLIENT:latest
                        docker run -d --name chat-server -p 5000:5000 $DOCKER_IMAGE_NAME_SERVER:latest
                    '''
                }
            }
        }
    }
}
