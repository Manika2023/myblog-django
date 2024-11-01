# Use an official Python image as a base
FROM python:3.10-slim

# Install system dependencies needed for building packages
# RUN apt-get update && \
#     apt-get install -y gcc build-essential pkg-config && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*
# Install system dependencies needed for building packages
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev build-essential pkg-config && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Set the working directory
WORKDIR /miniblog-django

# Copy only requirements.txt first to leverage Docker's cache
COPY requirements.txt .

# Install Python dependencies (include Gunicorn for production)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Copy the rest of the project files to the Docker image
COPY . .

# Expose the port (this step is optional for Railway as it uses environment variables)
EXPOSE 8000

# Run Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "miniblog2.wsgi:application"]