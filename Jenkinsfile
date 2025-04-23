pipeline {
    agent any

    environment {
        REGISTRY = "hariharan1112"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/HARIHARANJAYARAJ/hii.git', branch: 'main', credentialsId: 'github-pat'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    def services = ['chat-client', 'chat-server', 'chat-web']
                    services.each { service ->
                        sh "docker build -t $REGISTRY/${service}:latest ${service}"
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
                sh 'docker-compose up -d'
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
