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
                echo 'Installing Python dependencies...'
                sh 'pip3 install -r requirements.txt'
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
                sh 'docker run --rm uptime-bot:latest'
            }
        }
    }
}