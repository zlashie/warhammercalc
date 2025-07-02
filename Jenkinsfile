pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHONPATH = "${env.WORKSPACE}\\etl"

        // Inject prod DB credentials from Jenkins secret text credentials
        DB_NAME     = credentials('WAR_DB_NAME')
        DB_USER     = credentials('WAR_DB_USER')
        DB_PASSWORD = credentials('WAR_DB_PASSWORD')
        DB_HOST     = credentials('WAR_DB_HOST')
        DB_PORT     = credentials('WAR_DB_PORT')
    }

    stages {
        stage('Setup Python') {
            steps {
                // Create virtual environment
                bat 'C:\\Users\\tommy\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m venv venv'

                // Upgrade pip and install requirements
                bat '.\\venv\\Scripts\\python.exe --version'
                bat '.\\venv\\Scripts\\pip.exe install --upgrade pip'
                bat '.\\venv\\Scripts\\pip.exe install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Pytest will use tests/.env.test via dotenv in conftest.py
                bat 'if not exist tests\\reports mkdir tests\\reports'
                bat '.\\venv\\Scripts\\pytest.exe --cov=etl --cov-report=term --junitxml=tests/reports/results.xml'
            }
        }

        stage('Run ETL') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'WAR_DB_NAME', variable: 'DB_NAME'),
                    string(credentialsId: 'WAR_DB_USER', variable: 'DB_USER'),
                    string(credentialsId: 'WAR_DB_PASSWORD', variable: 'DB_PASSWORD'),
                    string(credentialsId: 'WAR_DB_HOST', variable: 'DB_HOST'),
                    string(credentialsId: 'WAR_DB_PORT', variable: 'DB_PORT')
                ]) {
                    script {
                        def output = bat(
                            script: '''
                            @echo off
                            .\\venv\\Scripts\\python.exe -m etl.main
                            ''',
                            returnStdout: true,
                            label: 'Running ETL pipeline...'
                        ).trim()

                        echo "\n================================"
                        echo "\n${output}"
                        echo "\n================================"
                    }
                }
            }
        }
    }

    post {
        always {
            junit 'tests/reports/*.xml'
        }
    }
}
