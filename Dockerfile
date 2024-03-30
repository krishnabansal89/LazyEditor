# Use the latest Python image as the base image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the required files to the container
COPY image_to_video.py server.py ./

# Copy the requirements file (if you have one)
COPY requirements.txt ./
COPY fullchain.pem /certs/
COPY privkey.pem /certs/

# Install the Python dependencies
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y  # for cv2
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your FastAPI app will run on (replace 8000 with the appropriate port)
EXPOSE 8000

# Set the command to run when the container starts
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/certs/privkey.pem", "--ssl-certfile", "/certs/fullchain.pem"]