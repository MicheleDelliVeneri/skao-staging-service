# Use a lightweight Python base image
# Use a Python 3.13 base image
FROM python:3.13-slim

# Create a working directory
WORKDIR /app

# Copy requirement definitions
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app

# Expose the application port (change if needed)
EXPOSE 8000

# By default, run the application with uvicorn
CMD ["uvicorn", "app.staging_service:app", "--host", "0.0.0.0", "--port", "8000"]