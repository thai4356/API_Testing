properties([
    pipelineTriggers([githubPush()])
])

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'echo "Building..."'
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Running tests..."'
            }
        }
    }
    post {
        success {
            githubNotify context: 'CI/CD', status: 'SUCCESS', description: 'Build passed'
        }
        failure {
            githubNotify context: 'CI/CD', status: 'FAILURE', description: 'Build failed'
        }
    }
}
