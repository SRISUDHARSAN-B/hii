pipeline {
    agent any

    environment {
        REGISTRY = "hariharan1112"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/HARIHARANJAYARAJ/realtime-docker-chat-app.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    def services = ['chat-client', 'chat-server', 'chat-web']
                    services.each { service ->
                        sh "docker build -t $REGISTRY/${service}:latest realtime-docker-chat-app/${service}"
                    }
                }
            }
        }

        stage('Push Images to DockerHub') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub-creds', url: '']) {
                    script {
                        def services = ['chat-client', 'chat-server', 'chat-web']
                        services.each { service ->
                            sh "docker push $REGISTRY/${service}:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy Using Docker Compose') {
            steps {
                sh 'docker-compose -f realtime-docker-chat-app/docker-compose.yml up -d'
            }
        }
    }

    post {
        success {
            echo "✅ Deployment complete!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
