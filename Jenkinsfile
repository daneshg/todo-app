pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                dir('todo_list'){
                    sh 'coverage run --source=base ./manage.py test'
                }
            }
        }
        stage('ViewReport'){
            steps{
                dir('todo_list'){
                    sh 'coverage report'
                }
            }
        }
    }
}