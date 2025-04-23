pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📦 Checking out source code...'
                git 'https://github.com/hariharan1112/chat-app'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    def services = ['chat-client', 'chat-server', 'chat-web']
                    for (service in services) {
                        dir(service) {
                            sh """
                                echo 🛠️ Building ${service}...
                                docker build -t hariharan1112/${service}:latest .
                            """
                        }
                    }
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo '🔐 Logging into Docker Hub...'
                sh 'echo "$DOCKER_HUB_CREDENTIALS_PSW" | docker login -u "$DOCKER_HUB_CREDENTIALS_USR" --password-stdin'
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    def services = ['chat-client', 'chat-server', 'chat-web']
                    for (service in services) {
                        sh """
                            echo 📤 Pushing ${service} to Docker Hub...
                            docker push hariharan1112/${service}:latest
                        """
                    }
                }
            }
        }

        stage('Ensure Network') {
            steps {
                echo '🔗 Checking or creating Docker network...'
                sh '''
                    docker network ls --format {{.Name}} | grep -q ^chat-network$ || docker network create chat-network
                '''
            }
        }

        stage('Deploy Containers') {
            steps {
                echo '🚀 Deploying containers...'
                sh '''
                    docker rm -f chat-client || true
                    docker rm -f chat-server || true
                    docker rm -f chat-web || true

                    docker run -d --network chat-network --name chat-server hariharan1112/chat-server:latest
                    docker run -d --network chat-network --name chat-client hariharan1112/chat-client:latest
                    docker run -d --network chat-network -p 8080:80 --name chat-web hariharan1112/chat-web:latest
                '''
            }
        }

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning up unused Docker resources...'
                sh 'docker system prune -f'
            }
        }

        stage('Success') {
            steps {
                echo '✅ CI/CD Pipeline completed successfully! Chat App is deployed and running.'
            }
        }
    }
}
