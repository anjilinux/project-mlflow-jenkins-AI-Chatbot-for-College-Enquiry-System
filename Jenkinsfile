pipeline {
    agent { label "gpu-node" }

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
        VECTORIZER_PATH = "vectorizer.pkl"

        PYTHONPATH = "${WORKSPACE}"
    }

    stages {

        stage("Stage 1: Checkout Code") {
            steps {
                sh '''
                /* ================================
                   Stage 1: Checkout Code
                ================================= */
                git branch: 'master',
                    url: 'https://github.com/anjilinux/project-mlflow-jenkins-AI-Chatbot-for-College-Enquiry-System.git'
                '''
            }
        }

        stage("Stage 2: Setup Virtual Environment") {
            steps {
                sh '''
                /* ================================
                   Stage 2: Setup Virtual Environment
                ================================= */
                set -e
                if [ ! -d venv ]; then
                    python3 -m venv venv
                fi
                venv/bin/pip install --upgrade pip
                venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage("Stage 3: Data Validation") {
            steps {
                sh '''
                /* ================================
                   Stage 3: Data Validation
                ================================= */
                set -e
                test -f college_faq.csv || (echo "CSV missing" && exit 1)
                venv/bin/python - <<EOF
import pandas as pd
df = pd.read_csv("college_faq.csv")
if not {"question","intent"}.issubset(df.columns):
    raise ValueError("Missing required columns")
if df.isnull().any().any():
    raise ValueError("Null values found")
print("✅ Dataset validation passed")
EOF
                '''
            }
        }

        stage("Stage 4: Data Collection") {
            steps {
                sh '''
                /* ================================
                   Stage 4: Data Collection
                ================================= */
                set -e
                venv/bin/python collect_data.py
                '''
            }
        }

        stage("Stage 5: Data Preprocessing") {
            steps {
                sh '''
                /* ================================
                   Stage 5: Data Preprocessing
                ================================= */
                set -e
                venv/bin/python preprocess.py
                '''
            }
        }

        stage("Stage 6: Feature Engineering") {
            steps {
                sh '''
                /* ================================
                   Stage 6: Feature Engineering
                ================================= */
                set -e
                venv/bin/python feature_engineering.py
                '''
            }
        }

        stage("Stage 7: Model Training (MLflow)") {
            steps {
                sh '''
                /* ================================
                   Stage 7: Model Training (MLflow)
                ================================= */
                set -e
                export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                export MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
                venv/bin/python train.py
                '''
            }
        }

        stage("Stage 8: Model Evaluation") {
            steps {
                sh '''
                /* ================================
                   Stage 8: Model Evaluation
                ================================= */
                set -e
                venv/bin/python evaluate.py
                '''
            }
        }

        stage("Stage 9: Run PyTests") {
            steps {
                sh '''
                /* ================================
                   Stage 9: Run PyTests
                ================================= */
                set -e
                venv/bin/pytest tests/ --disable-warnings
                '''
            }
        }

        stage("Stage 10: Model Artifact Check") {
            steps {
                sh '''
                /* ================================
                   Stage 10: Model Artifact Check
                ================================= */
                set -e
                test -f $MODEL_PATH || exit 1
                test -f $VECTORIZER_PATH || exit 1
                echo "✅ Model artifacts verified"
                '''
            }
        }

        stage("Stage 11: FastAPI Local Smoke Test") {
            steps {
                sh '''
                /* ================================
                   Stage 11: FastAPI Local Smoke Test
                ================================= */
                set -e
                echo "🚀 Checking GPU with nvidia-smi before FastAPI..."
                nvidia-smi

                echo "🚀 Starting FastAPI..."
                venv/bin/uvicorn main:app --host 0.0.0.0 --port $APP_PORT > uvicorn.log 2>&1 &
                PID=$!

                echo "⏳ Waiting for FastAPI health endpoint..."
                for i in {1..15}; do
                    if curl -sf http://localhost:$APP_PORT/health > /dev/null; then
                        echo "✅ FastAPI is healthy"
                        break
                    fi
                    sleep 5
                done

                echo "🤖 Running API predict test..."
                curl -X POST http://localhost:$APP_PORT/predict \
                    -H "Content-Type: application/json" \
                    -d '{"question":"Is hostel available?"}' | tee response.json

                kill $PID

                echo "🚀 GPU status after FastAPI test:"
                nvidia-smi
                '''
            }
        }

        stage("Stage 12: Docker Build") {
            steps {
                sh '''
                /* ================================
                   Stage 12: Docker Build
                ================================= */
                set -e
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage("Stage 13: Docker Smoke Test + AI Agent API Test") {
            steps {
                sh '''
                /* ================================
                   Stage 13: Docker Smoke Test + AI Agent API Test
                ================================= */
                set -e

                CONTAINER=college_chatbot_test
                docker rm -f $CONTAINER || true

                HOST_PORT=$(shuf -i 8000-8999 -n 1)
                echo "Using host port: $HOST_PORT"

                echo "🚀 GPU status before running Docker container:"
                nvidia-smi

                docker run --gpus all -d -p ${HOST_PORT}:8000 --name $CONTAINER $IMAGE_NAME:$IMAGE_TAG

                echo "⏳ Waiting for container health..."
                for i in $(seq 1 20); do
                    if curl -sf http://localhost:${HOST_PORT}/health; then
                        echo "✅ Container is healthy"
                        break
                    fi
                    nvidia-smi
                    sleep 5
                done

                echo "🤖 Testing AI Agent predict API inside Docker..."
                curl -X POST http://localhost:${HOST_PORT}/predict \
                    -H "Content-Type: application/json" \
                    -d '{"question":"Is hostel available?"}' | tee response.json

                echo "📜 Container logs:"
                docker logs $CONTAINER

                echo "🚀 GPU status after Docker container test:"
                nvidia-smi

                docker rm -f $CONTAINER
                '''
            }
        }

        stage("Stage 14: Archive Artifacts") {
            steps {
                sh '''
                /* ================================
                   Stage 14: Archive Artifacts
                ================================= */
                '''
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
