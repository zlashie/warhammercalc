pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DB_ENV_FILE = '.env'
    }

    stages {
        stage('Setup Python') {
            steps {
                // Use the full path to create the virtual environment
                bat 'C:\\Users\\tommy\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m venv venv'


                // Activate venv and install requirements
                bat '.\\venv\\Scripts\\python.exe --version'
                bat '.\\venv\\Scripts\\pip install --upgrade pip'
                bat '.\\venv\\Scripts\\pip install -r requirements.txt'
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
