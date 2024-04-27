# Use the official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (required for some Python packages like pandas/scikit-learn sometimes depending on wheel availability)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Healthcheck to verify Streamlit is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
