# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the application files
COPY requirements.txt pyproject.toml /app/
COPY alembic.ini /app/
COPY .env /app/
COPY /src /app/src
COPY /tests /app/tests
COPY /migrations /app/migrations
COPY /init-db /app/init-db

# Set working directory
WORKDIR /app

# Install Python dependencies (online)
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Command to run your application
ENTRYPOINT [ "" ]