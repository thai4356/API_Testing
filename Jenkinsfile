pipeline {
    agent any

    triggers {
        githubPush()   // nếu GitHub
        // gitlab(triggerOnPush: true, triggerOnMergeRequest: true) // nếu GitLab
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "Building project..."
                // Ví dụ: sh 'mvn clean install' hoặc npm install && npm run build
            }
        }

        stage('Test') {
            steps {
                echo "Running tests..."
                // Ví dụ: sh 'mvn test'
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying..."
            }
        }
    }
}
