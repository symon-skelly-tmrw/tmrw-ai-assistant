
# Use the official Python image from the Docker Hub
FROM python:3.13-slim

# Set environment variables
ENV RESOLUTION=1920x1080x24
ENV RESOLUTION_WIDTH=1920
ENV RESOLUTION_HEIGHT=1080
ENV BROWSER_HEADLESS=true

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libgbm1 \
    libpango-1.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libxdamage1 \
    libxshmfence1 \
    libnspr4 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

RUN pip install browser-use

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir playwright==1.49.0 && \
    playwright install --with-deps chromium && \
    playwright install-deps

# Expose the port the app runs on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py"]
