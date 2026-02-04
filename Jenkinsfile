pipeline {
    agent {
        label "gpu-node"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        PYTHON = "python3"
        VENV_DIR = "venv"
        APP_PORT = "7000"

        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "AI-College-Enquiry-Chatbot"

        IMAGE_NAME = "college-enquiry-chatbot"
        IMAGE_TAG = "latest"

        MODEL_PATH = "model.pkl"
        VECTORIZER_PATH = "artifacts/vectorizer.pkl"

        PYTHONPATH = "${WORKSPACE}"
    }

    stages {

        stage("Checkout Code") {
            steps {
                git branch: 'master',
                    url: 'https://github.com/anjilinux/project-mlflow-jenkins-AI-Chatbot-for-College-Enquiry-System.git'
            }
        }

        stage("Setup Virtual Environment") {
            steps {
                sh '''
                    set -e
                    if [ ! -d venv ]; then
                        python3 -m venv venv
                    fi
                   
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage("Data Validation") {
            steps {
                sh '''
                    set -e
                    echo "🔍 Validating dataset..."

                    test -f college_faq.csv || (echo "CSV missing" && exit 1)

                    venv/bin/python - <<EOF
import pandas as pd

df = pd.read_csv("college_faq.csv")

if not {"question", "intent"}.issubset(df.columns):
    raise ValueError("Missing required columns")

if df.isnull().any().any():
    raise ValueError("Null values found")

print("✅ Dataset validation passed")
EOF
                '''
            }
        }

        stage("Data Collection") {
            steps {
                sh '''
                    set -e
                    venv/bin/python collect_data.py
                '''
            }
        }

        stage("Data Preprocessing") {
            steps {
                sh '''
                    set -e
                    venv/bin/python preprocess.py
                '''
            }
        }

        stage("Feature Engineering") {
            steps {
                sh '''
                    set -e
                    venv/bin/python feature_engineering.py
                '''
            }
        }

        stage("Model Training (MLflow)") {
            steps {
                sh '''
                    set -e
                    export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                    export MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
                    venv/bin/python train.py
                '''
            }
        }

        stage("Model Evaluation") {
            steps {
                sh '''
                    set -e
                    venv/bin/python evaluate.py
                '''
            }
        }

        stage("Run PyTests") {
            steps {
                sh '''
                    set -e
                    venv/bin/pytest tests/ --disable-warnings
                '''
            }
        }

        stage("Model Artifact Check") {
            steps {
                sh '''
                    set -e
                    test -f $MODEL_PATH || exit 1
                    test -f $VECTORIZER_PATH || exit 1
                    echo "✅ Model artifacts verified"
                '''
            }
        }

        stage("FastAPI Smoke Test (Local)") {
            steps {
                sh '''
                    set -e
                    . venv/bin/activate

                    echo "🚀 Starting FastAPI..."
                    uvicorn main:app --host 0.0.0.0 --port $APP_PORT > uvicorn.log 2>&1 &
                    PID=$!

                    for i in {1..20}; do
                        if curl -s http://localhost:$APP_PORT/health | grep -q ok; then
                            kill $PID
                            exit 0
                        fi
                        sleep 2
                    done

                    cat uvicorn.log
                    kill $PID || true
                    exit 1
                '''
            }
        }

        stage("Docker Build") {
            steps {
                sh '''
                    set -e
                    docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage("Docker Smoke Test") {
            steps {
                sh '''
                    set -e
                    CONTAINER=college_chatbot_test
                    docker rm -f $CONTAINER || true

                    HOST_PORT=$(shuf -i 8000-8999 -n 1)
                    docker run -d -p $HOST_PORT:$APP_PORT --name $CONTAINER $IMAGE_NAME:$IMAGE_TAG

                    for i in {1..30}; do
                        if curl -s http://localhost:$HOST_PORT/health | grep -q ok; then
                            docker rm -f $CONTAINER
                            exit 0
                        fi
                        sleep 1
                    done

                    docker logs $CONTAINER
                    docker rm -f $CONTAINER
                    exit 1
                '''
            }
        }

        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: '''
                    artifacts/*.pkl,
                    mlruns/**,
                    uvicorn.log
                ''', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ College Enquiry Chatbot Pipeline SUCCESS"
        }
        failure {
            echo "❌ College Enquiry Chatbot Pipeline FAILED"
        }
    }
}
