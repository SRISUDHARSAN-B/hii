pipeline {
  agent any

  environment {
    REGISTRY     = 'hariharan1112' // Your Docker Hub username
    CLIENT_IMAGE = "${REGISTRY}/chat-client:latest"
    SERVER_IMAGE = "${REGISTRY}/chat-server:latest"
    WEB_IMAGE    = "${REGISTRY}/chat-web:latest"
    DOCKER_CREDS = 'dockerhub-creds' // Jenkins credential ID for Docker Hub login
  }

  stages {

    stage('Checkout') {
      steps {
        echo '📦 Checking out code...'
        checkout scm // Checks out the source code from the configured SCM
      }
    }

    stage('Ensure Network') {
      steps {
        echo '🔗 Ensuring Docker network exists...'
        sh '''
          # Check if the custom network exists, if not, create it
          if ! docker network ls --format '{{.Name}}' | grep -q '^chat_network$'; then
            docker network create chat_network
          fi
        '''
      }
    }

    stage('Build Images') {
      steps {
        echo '🛠️ Building Docker images...'
        script {
          def services = [
            'chat-client': CLIENT_IMAGE,
            'chat-server': SERVER_IMAGE,
            'chat-web': WEB_IMAGE
          ]
          for (svcDir in services.keySet()) {
            def imageTag = services[svcDir]
            sh """
              echo "🔨 Building ${svcDir}..."
              # Build each service using its respective directory as the build context
              docker build -t ${imageTag} ./${svcDir}
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
            # Log in to Docker Hub using Jenkins credentials
            echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
            # Push all built images to Docker Hub
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
          # Stop and remove any existing containers defined in docker-compose.yml
          # --remove-orphans removes services not defined in the compose file
          docker compose down --remove-orphans || true
          # Start all services in detached mode based on docker-compose.yml
          docker compose up -d
        '''
      }
    }
  }

  post {
    success {
      echo "✅ Deployed all services on chat_network successfully!"
    }
    failure {
      echo "❌ Pipeline failed — check the logs above."
    }
    always {
      echo "🔁 Pipeline execution completed."
    }
  }
}