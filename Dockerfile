FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg git

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
