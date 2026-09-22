pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t uptime-bot:latest .'
            }
        }

        stage('Docker Run') {
            steps {
                echo 'Running the container...'
                withCredentials([string(credentialsId: 'slack-webhook-url', variable: 'SLACK_WEBHOOK_URL')]) {
                    sh 'docker run --rm -e SLACK_WEBHOOK_URL="$SLACK_WEBHOOK_URL" uptime-bot:latest'
                }
            }
        }
    }
}