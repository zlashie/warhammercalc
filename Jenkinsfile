pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DB_ENV_FILE = '.env'
    }

    stages {
        stage('Setup Python') {
            steps {
                bat "python -m venv %VENV_DIR%"
                bat "%VENV_DIR%\\Scripts\\pip install --upgrade pip"
                bat "%VENV_DIR%\\Scripts\\pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                bat "%VENV_DIR%\\Scripts\\pytest --cov=etl --cov-report=term"
            }
        }

        stage('Run ETL') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                bat """
                setlocal EnableDelayedExpansion
                for /f "usebackq tokens=1,2 delims==" %%A in (%DB_ENV_FILE%) do (
                    set %%A=%%B
                )
                call %VENV_DIR%\\Scripts\\python etl\\main.py
                endlocal
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
