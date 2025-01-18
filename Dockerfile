# Use a lightweight Python base image
# Use a Python 3.13 base image

# Build React frontend
FROM node:18 AS frontend
WORKDIR /frontend
# Copy React files and install dependencies
COPY frontend/package.json frontend/package-lock.json /frontend/
RUN npm install
# Build the React application
COPY frontend /frontend
RUN npm run build

# Build FastAPI backend

FROM python:3.13-slim AS backend

# Create a working directory
WORKDIR /app

# Copy requirement definitions
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app
COPY app /app/app
COPY --from=frontend /frontend/build /app/frontend/build
# Expose the application port (change if needed)
EXPOSE 8000

# By default, run the application with uvicorn
CMD ["uvicorn", "app.staging_service:app", "--host", "0.0.0.0", "--port", "8000"]