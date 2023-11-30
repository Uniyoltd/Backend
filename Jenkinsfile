pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Uniyoltd/backend.git'
            }
        }

        stage('Collect static files') {
            steps {
                sh 'python manage.py collectstatic'
            }
        }

        stage('Run migrations') {
            steps {
                sh 'python manage.py makemigrations'
                sh 'python manage.py migrate'
            }
        }

        stage('Deploy') {
            steps {
                sh 'sudo service gunicorn restart'
            }
        }
    }
}
