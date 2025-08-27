FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Create uploads folder with proper permissions
RUN mkdir -p /app/uploads && chmod -R 777 /app/uploads

# Expose port
EXPOSE 7860

# Run the app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
