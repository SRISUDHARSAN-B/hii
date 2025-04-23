pipeline {
  agent any

  environment {
    REGISTRY = 'hariharan1112'
    CLIENT_IMAGE = "${REGISTRY}/chat-client:latest"
    SERVER_IMAGE = "${REGISTRY}/chat-server:latest"
    WEB_IMAGE    = "${REGISTRY}/chat-web:latest"
  }

  stages {
    stage('Checkout') {
      steps {
        // Jenkins will clone your repo into the workspace
        checkout scm
      }
    }

    stage('Build Docker Images') {
      steps {
        script {
          def services = ['chat-client', 'chat-server', 'chat-web']
          services.each { svc ->
            sh """
              echo "— Building image for ${svc} —"
              docker build -t ${REGISTRY}/${svc}:latest ./${svc}
            """
          }
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        // Uses the "dockerhub-creds" credential you added in Jenkins
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                         usernameVariable: 'DOCKERHUB_USER',
                                         passwordVariable: 'DOCKERHUB_PASS')]) {
          sh '''
            echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
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
          # Stop and remove old containers if they exist
          docker rm -f chat-client chat-server chat-web || true

          # Run new ones
          docker run -d --name chat-client -p 3000:3000 ${CLIENT_IMAGE}
          docker run -d --name chat-server -p 5000:5000 ${SERVER_IMAGE}
          docker run -d --name chat-web    -p 80:80    ${WEB_IMAGE}
        '''
      }
    }
  }

  post {
    success { echo "✅ All stages completed — your chat app is live!" }
    failure { echo "❌ Pipeline failed. Check the logs above." }
  }
}
