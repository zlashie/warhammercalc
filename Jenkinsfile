pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DB_ENV_FILE = '.env'
        PYTHONPATH = "${env.WORKSPACE}\\etl"
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
                bat '.\\venv\\Scripts\\pytest.exe --cov=etl --cov-report=term'
            }
        }

        stage('Run ETL') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                bat """
                for /f "usebackq tokens=* delims=" %%a in (".env") do set %%a
                .\\venv\\Scripts\\python.exe etl\\main.py
                """
            }
        }
    }

    post {
        always {
            // Optional: only works if you output XMLs in pytest
            junit 'tests/reports/*.xml'
        }
    }
}
