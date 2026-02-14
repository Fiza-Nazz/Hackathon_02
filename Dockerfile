FROM python:3.11

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from both folders
COPY ./backend/requirements.txt /code/requirements_backend.txt
COPY ./Chatbot/requirements.txt /code/requirements_chatbot.txt

# Install dependencies in one layer to keep image clean
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /code/requirements_backend.txt && \
    pip install --no-cache-dir -r /code/requirements_chatbot.txt && \
    pip install --no-cache-dir groq openai uvicorn sqlmodel asyncpg psycopg2-binary python-dotenv

# Copy ALL code into /code
COPY . /code/

# Set PYTHONPATH to include /code
ENV PYTHONPATH=/code

# Use uvicorn with proxy entry point approach
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
