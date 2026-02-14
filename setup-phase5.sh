#!/bin/bash

# Phase V Setup Script
# This script sets up the complete Phase V environment

set -e

echo "🚀 Phase V Setup Script"
echo "======================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose found${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found${NC}"

# Step 1: Start Docker services
echo -e "\n${YELLOW}Step 1: Starting Docker services...${NC}"
docker-compose up -d
echo -e "${GREEN}✅ Docker services started${NC}"

# Wait for services to be ready
echo -e "\n${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

# Step 2: Setup backend
echo -e "\n${YELLOW}Step 2: Setting up backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python -m src.database.init_db

cd ..
echo -e "${GREEN}✅ Backend setup complete${NC}"

# Step 3: Create Kafka topics
echo -e "\n${YELLOW}Step 3: Creating Kafka topics...${NC}"
docker exec todo_redpanda rpk topic create task-events --brokers=localhost:9092 || true
docker exec todo_redpanda rpk topic create reminders --brokers=localhost:9092 || true
docker exec todo_redpanda rpk topic create task-updates --brokers=localhost:9092 || true
echo -e "${GREEN}✅ Kafka topics created${NC}"

# Step 4: Verify services
echo -e "\n${YELLOW}Step 4: Verifying services...${NC}"

# Check PostgreSQL
if docker exec todo_postgres pg_isready -U todouser &> /dev/null; then
    echo -e "${GREEN}✅ PostgreSQL is ready${NC}"
else
    echo -e "${RED}❌ PostgreSQL is not ready${NC}"
fi

# Check Redpanda
if docker exec todo_redpanda rpk cluster info --brokers=localhost:9092 &> /dev/null; then
    echo -e "${GREEN}✅ Redpanda is ready${NC}"
else
    echo -e "${RED}❌ Redpanda is not ready${NC}"
fi

# Step 5: Display service URLs
echo -e "\n${GREEN}✅ Phase V Setup Complete!${NC}"
echo -e "\n${YELLOW}Service URLs:${NC}"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "  Redpanda Console: http://localhost:8080"
echo "  PostgreSQL: localhost:5432"
echo "  Kafka Brokers: localhost:19092"

echo -e "\n${YELLOW}Next steps:${NC}"
echo "  1. Start backend: cd backend && source venv/bin/activate && uvicorn src.main:app --reload"
echo "  2. Start frontend: cd frontend && npm start"
echo "  3. Start chatbot: cd Chatbot && python app.py"
echo "  4. Access API: http://localhost:8000/docs"

echo -e "\n${YELLOW}To stop services:${NC}"
echo "  docker-compose down"

echo -e "\n${YELLOW}To view logs:${NC}"
echo "  docker-compose logs -f"
