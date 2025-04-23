pipeline {
    agent any

    environment {
        DOCKER_IMAGE_CLIENT = 'hariharan1112/chat-client:latest'
        DOCKER_IMAGE_SERVER = 'hariharan1112/chat-server:latest'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Clone Repository') {
            steps {
                sh 'rm -rf ChatApp || true'
                sh 'git clone https://github.com/your-username/ChatApp.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                dir('ChatApp/chat-client') {
                    sh 'docker build -t ${DOCKER_IMAGE_CLIENT} .'
                }
                dir('ChatApp/chat-server') {
                    sh 'docker build -t ${DOCKER_IMAGE_SERVER} .'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh '''
                        echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push ${DOCKER_IMAGE_CLIENT}
                        docker push ${DOCKER_IMAGE_SERVER}
                    '''
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                sh '''
                    docker rm -f chat-client || true
                    docker rm -f chat-server || true

                    docker run -d --name chat-client -p 3000:3000 ${DOCKER_IMAGE_CLIENT}
                    docker run -d --name chat-server -p 5000:5000 ${DOCKER_IMAGE_SERVER}
                '''
            }
        }
    }
}
