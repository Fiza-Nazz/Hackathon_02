FROM python:3.11

WORKDIR /code

# Sabse pehle backend folder se requirements copy karein
COPY ./backend/requirements.txt /code/requirements.txt

# Dependencies install karein
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Sirf backend ka code copy karein code folder mein
COPY ./backend /code

# Environment variables ke liye defaults (optional)
ENV PORT=7860

# Backend start karein
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
