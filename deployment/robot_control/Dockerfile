FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for MuJoCo (rendering support if needed usually requires more, but for headless physics these are fine)
# We might need libgl1-mesa-glx for some contexts, but let's start minimal.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libglfw3 \
    libglew2.2 \
    && rm -rf /var/lib/apt/lists/*

# Install MuJoCo python bindings and websockets
RUN pip install mujoco numpy websockets

# Copy script
COPY main.py .

CMD ["python", "-u", "main.py"]
