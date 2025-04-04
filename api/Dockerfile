FROM python:3.12

WORKDIR /

# Copy the dependencies file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set Flask environment variable
ENV FLASK_APP=index.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
