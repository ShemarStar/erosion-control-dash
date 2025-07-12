# Use the official Python 3.13 image as the base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Streamlit uses (default 8501, but Render uses $PORT)
EXPOSE $PORT

# Run the Streamlit app
CMD ["streamlit", "run", "dashboard.py", "--server.port", "$PORT", "--server.address", "0.0.0.0"]
