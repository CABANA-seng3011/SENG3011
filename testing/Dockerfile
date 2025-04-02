FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
COPY tests ./tests
COPY src ./src  # Copy the microservice source code

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set entrypoint to run tests
CMD ["pytest", "tests", "--cov=src", "--cov-report=term-missing"]