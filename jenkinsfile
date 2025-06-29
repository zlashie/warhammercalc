pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DB_ENV_FILE = '.env'  
    }

    stages {
        stage('Setup Python') {
            steps {
                sh 'python -m venv $VENV_DIR'
                sh './$VENV_DIR/bin/pip install --upgrade pip'
                sh './$VENV_DIR/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh './$VENV_DIR/bin/pytest --cov=etl --cov-report=term'
            }
        }

        stage('Run ETL') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                sh '''
                set -a
                source ${DB_ENV_FILE}
                set +a
                ./$VENV_DIR/bin/python etl/main.py
                '''
            }
        }
    }

    post {
        always {
            junit 'tests/reports/*.xml' 
        }
    }
}
