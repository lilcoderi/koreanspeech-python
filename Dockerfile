FROM python:3.10-slim

# Install ffmpeg dan system tools
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Salin requirements
COPY requirements.txt .

# Install torch CPU dari index khusus
RUN pip install --no-cache-dir torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Install sisa dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh app
COPY . .

# Expose port
EXPOSE 5000

# Jalankan aplikasi
CMD ["python", "app.py"]
