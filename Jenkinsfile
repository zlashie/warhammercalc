pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DB_ENV_FILE = '.env'
    }

    stages {
        stage('Setup Python') {
            steps {
                bat 'python --version' 
                bat 'python -m venv %VENV_DIR%'
                bat '%VENV_DIR%\\Scripts\\pip install --upgrade pip'
                bat '%VENV_DIR%\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '%VENV_DIR%\\Scripts\\pytest --cov=etl --cov-report=term'
            }
        }

        stage('Run ETL') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate
                %VENV_DIR%\\Scripts\\python etl\\main.py
                """
            }
        }
    }

    post {
        always {
            junit 'tests/reports/*.xml'
        }
    }
}
