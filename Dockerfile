FROM python:3.10-slim

# Install ffmpeg & dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .

# Install torch (versi ringan)
RUN pip install --no-cache-dir torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Run app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
