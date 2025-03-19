FROM python:3.12

WORKDIR /

# Install dependencies
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Set the Flask app environment variable
ENV FLASK_APP=index.py

EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]