# Use a minimal Python 3.9 base image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy all deployment files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit default port (HF Spaces uses 7860)
EXPOSE 7860

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
