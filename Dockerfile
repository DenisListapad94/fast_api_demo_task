FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1



COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR source
COPY . /source
# CMD ["uvicorn", "src.main:app","--reload"]