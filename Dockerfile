# Gunakan image Python ringan
FROM python:3.10-slim

# Install ffmpeg dan dependency sistem minimal
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Tentukan direktori kerja
WORKDIR /app

# Salin file requirements.txt dan install dependency Python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file project ke direktori kerja
COPY . .

# Buka port Flask default
EXPOSE 5000

# Jalankan aplikasi
CMD ["python", "app.py"]
