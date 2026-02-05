pipeline {
    agent {
        label "gpu-node"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 90, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '15'))
    }

    environment {
        PYTHON = "python3.12"
        VENV_DIR = "venv"
        APP_PORT = "8000"

        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "AI-College-Enquiry-Chatbot"

        IMAGE_NAME = "college-enquiry-chatbot"
        IMAGE_TAG = "latest"

        MODEL_PATH = "model.pkl"
        VECTORIZER_PATH = "vectorizer.pkl"

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
                    if [ ! -d $VENV_DIR ]; then
                        $PYTHON -m venv $VENV_DIR
                    fi
                    $VENV_DIR/bin/pip install --upgrade pip
                    $VENV_DIR/bin/pip install -r requirements.txt
                '''
            }
        }

        stage("Data Validation") {
            steps {
                sh '''
                    set -e
                    echo "🔍 Validating dataset..."
                    test -f college_faq.csv || (echo "CSV missing" && exit 1)

                    $VENV_DIR/bin/python - <<EOF
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
                    $VENV_DIR/bin/python collect_data.py
                '''
            }
        }

        stage("Data Preprocessing") {
            steps {
                sh '''
                    set -e
                    $VENV_DIR/bin/python preprocess.py
                '''
            }
        }

        stage("Feature Engineering") {
            steps {
                sh '''
                    set -e
                    $VENV_DIR/bin/python feature_engineering.py
                '''
            }
        }

        stage("Model Training (MLflow)") {
            steps {
                sh '''
                    set -e
                    export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                    export MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
                    $VENV_DIR/bin/python train.py
                '''
            }
        }

        stage("Model Evaluation") {
            steps {
                sh '''
                    set -e
                    $VENV_DIR/bin/python evaluate.py
                '''
            }
        }

        stage("Run PyTests") {
            steps {
                sh '''
                    set -e
                    $VENV_DIR/bin/pytest tests/ --disable-warnings
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

        stage('Docker Build') {
            steps {
                sh '''
                    set -e
                    docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        
stage("Docker GPU Smoke Test + AI Agent API Test") {
    steps {
        sh '''
        set -e

        CONTAINER=college_chatbot_test
        docker rm -f $CONTAINER || true

        HOST_PORT=$(shuf -i 8000-8999 -n 1)
        echo "Using host port: $HOST_PORT"

        echo "📊 GPU usage BEFORE starting container"
        nvidia-smi

        # Run container with GPU support, map to 8000 inside
        docker run --gpus all -d -p ${HOST_PORT}:8000 --name $CONTAINER college-enquiry-chatbot:latest

        echo "⏳ Waiting for container to become healthy..."
        for i in $(seq 1 20); do
            if curl -sf http://localhost:${HOST_PORT}/health > /dev/null; then
                echo "✅ Container is healthy"
                break
            fi
            sleep 5
        done

        echo "📊 GPU usage AFTER starting container"
        nvidia-smi

        echo "🤖 Testing AI Agent predict API..."
        curl -X POST http://localhost:${HOST_PORT}/predict \
            -H "Content-Type: application/json" \
            -d '{"question":"Is hostel available?"}' | tee response.json

        echo "📜 Container logs:"
        docker logs $CONTAINER

        echo "📊 GPU usage AFTER API test"
        nvidia-smi

        docker rm -f $CONTAINER
        '''
    }
}





        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: '''
                    artifacts/*.pkl,
                    mlruns/**,
                    uvicorn.log,
                    response.json
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
