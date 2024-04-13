FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the required files to the container
COPY image_to_video.py server.py ./

# Copy the requirements file (if you have one)
COPY requirements.txt ./


RUN mkdir -p /var/lib/apt/lists/partial
RUN apt-get update --fix-missing

# Install the Python dependencies
RUN apt-get install -y ffmpeg libsm6 libxext6

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your FastAPI app will run on (replace 8000 with the appropriate port)
EXPOSE 8000

# Set the command to run when the container starts
CMD ["uvicorn", "server:app", "--host", "0.0.0.0" ]
