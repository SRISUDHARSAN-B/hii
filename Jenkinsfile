pipeline {
  agent any

  environment {
    REGISTRY     = 'hariharan1112'
    CLIENT_IMAGE = "${REGISTRY}/chat-client:latest"
    SERVER_IMAGE = "${REGISTRY}/chat-server:latest"
    WEB_IMAGE    = "${REGISTRY}/chat-web:latest"
    DOCKER_CREDS = 'dockerhub-creds'
  }

  stages {

    stage('Checkout') {
      steps {
        echo '📦 Checking out code...'
        checkout scm
      }
    }

    stage('Ensure Network') {
      steps {
        echo '🔗 Ensuring Docker network exists...'
        sh '''
          if ! docker network ls --format '{{.Name}}' | grep -q '^chat-network$'; then
            docker network create chat-network
          fi
        '''
      }
    }

    stage('Build Images') {
      steps {
        echo '🛠️ Building Docker images...'
        script {
          def services = ['chat-client', 'chat-server', 'chat-web']
          for (svc in services) {
            sh """
              echo "🔨 Building ${svc}..."
              docker build --network=host -t ${REGISTRY}/${svc}:latest ./${svc}
            """
          }
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        echo '📤 Pushing images to Docker Hub...'
        withCredentials([usernamePassword(
          credentialsId: "${DOCKER_CREDS}",
          usernameVariable: 'DOCKERHUB_USER',
          passwordVariable: 'DOCKERHUB_PASS'
        )]) {
          sh '''
            echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
            docker push ${CLIENT_IMAGE}
            docker push ${SERVER_IMAGE}
            docker push ${WEB_IMAGE}
          '''
        }
      }
    }

    stage('Deploy') {
      steps {
        echo '🚀 Deploying containers...'
        sh '''
          docker rm -f chat-client chat-server chat-web || true

          docker run -d --name chat-server --network chat-network -p 5000:5000 ${SERVER_IMAGE}
          docker run -d --name chat-client --network chat-network -p 3000:3000 ${CLIENT_IMAGE}
          docker run -d --name chat-web    --network chat-network -p 80:80    ${WEB_IMAGE}
        '''
      }
    }
  }

  post {
    success {
      echo "✅ Deployed all services on chat-network successfully!"
    }
    failure {
      echo "❌ Pipeline failed — check the logs above."
    }
    always {
      echo "🔁 Pipeline execution completed."
    }
  }
}
