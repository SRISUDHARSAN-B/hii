pipeline {
  agent any

  environment {
    REGISTRY      = 'hariharan1112'
    CLIENT_IMAGE  = "${REGISTRY}/chat-client:latest"
    SERVER_IMAGE  = "${REGISTRY}/chat-server:latest"
    WEB_IMAGE     = "${REGISTRY}/chat-web:latest"
  }

  stages {
    stage('Checkout') {
      steps {
        // Pull down your repo (including Jenkinsfile)
        checkout scm
      }
    }

    stage('Cleanup Existing') {
      steps {
        sh '''
          # If you previously used docker-compose, tear it down
          docker-compose down || true

          # Remove any old containers by name
          docker rm -f chat-client chat-server chat-web || true
        '''
      }
    }

    stage('Build Docker Images') {
      steps {
        script {
          // Build each service from its subfolder
          ['chat-client','chat-server','chat-web'].each { svc ->
            sh """
              echo \"— Building ${svc} —\"
              docker build -t ${REGISTRY}/${svc}:latest ./${svc}
            """
          }
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        // Uses the credentials you added with ID "dockerhub-creds"
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                         usernameVariable: 'DOCKERHUB_USER',
                                         passwordVariable: 'DOCKERHUB_PASS')]) {
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
          # Run fresh containers on the desired ports
          docker run -d --name chat-client -p 3000:3000 ${CLIENT_IMAGE}
          docker run -d --name chat-server -p 5000:5000 ${SERVER_IMAGE}
          docker run -d --name chat-web    -p 80:80    ${WEB_IMAGE}
        '''
      }
    }
  }

  post {
    success { echo "✅ All done — your chat app is live!" }
    failure { echo "❌ Pipeline failed. Inspect the logs above." }
  }
}
