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
                withEnv([
                    'DB_NAME=' + env.DB_NAME,
                    'DB_USER=' + env.DB_USER,
                    'DB_PASSWORD=' + env.DB_PASSWORD,
                    'DB_HOST=' + env.DB_HOST,
                    'DB_PORT=' + env.DB_PORT
                ]) {
                    bat '.\\venv\\Scripts\\python.exe etl\\main.py'
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
