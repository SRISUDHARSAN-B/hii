pipeline {
  agent any

  environment {
    REGISTRY     = 'hariharan1112'
    CLIENT_IMAGE = "${REGISTRY}/chat-client:latest"
    SERVER_IMAGE = "${REGISTRY}/chat-server:latest"
    WEB_IMAGE    = "${REGISTRY}/chat-web:latest"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Images') {
      steps {
        script {
          // Build each service with host networking (so DNS works)
          ['chat-client','chat-server','chat-web'].each { svc ->
            sh """
              echo "— Building ${svc} —"
              docker build --network=host \\
                -t ${REGISTRY}/${svc}:latest ./${svc}
            """
          }
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'dockerhub-creds',
          usernameVariable: 'DOCKERHUB_USER',
          passwordVariable: 'DOCKERHUB_PASS'
        )]) {
          sh '''
            echo "$DOCKERHUB_PASS" \
              | docker login -u "$DOCKERHUB_USER" --password-stdin

            docker push ${CLIENT_IMAGE}
            docker push ${SERVER_IMAGE}
            docker push ${WEB_IMAGE}
          '''
        }
      }
    }

    stage('Deploy Containers') {
      steps {
        sh '''
          docker rm -f chat-client chat-server chat-web || true

          docker run -d --name chat-client -p 3000:3000 ${CLIENT_IMAGE}
          docker run -d --name chat-server -p 5000:5000 ${SERVER_IMAGE}
          docker run -d --name chat-web    -p 80:80    ${WEB_IMAGE}
        '''
      }
    }
  }

  post {
    success { echo "✅ Pipeline succeeded — your chat app is live!" }
    failure { echo "❌ Pipeline failed. Check above logs." }
  }
}
