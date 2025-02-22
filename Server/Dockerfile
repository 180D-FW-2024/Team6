FROM debian:bookworm-slim
RUN apt-get update
RUN apt-get install flac -y
RUN apt install python3-pip -y
RUN apt install python3.11-venv -y

WORKDIR /app
COPY requirements.txt .
RUN python3 -m venv my-venv
# Use virtual env
ENV PATH="my-venv/bin:$PATH" 

RUN pip3 install -r requirements.txt
RUN pip3 uninstall opencv-python -y
RUN pip3 install opencv-python-headless
COPY mongodb.py . 
COPY app.py .
COPY templates templates
EXPOSE 5002

CMD ["my-venv/bin/python3.11", "app.py"]

### Older (smaller) version: everything works except
# for speech recognition (flac dependency not installed
# on non mac/linux/windows systems)

# FROM python:3.12-slim-bookworm AS build

# RUN apt-get update && apt-get install -y gcc
# WORKDIR /app
# COPY requirements.txt .
# RUN pip3 install -r requirements.txt
# RUN pip3 uninstall opencv-python -y
# RUN pip3 install opencv-python-headless

# FROM python:3.12-slim-bookworm
# WORKDIR /app
# COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
# COPY --from=flac_build /usr/bin/flac /usr/bin/flac
# COPY mongodb.py . 
# COPY app.py .
# # COPY vgg_face_weights.h5 /root/.deepface/weights/vgg_face_weights.h5
# COPY templates templates
# EXPOSE 5002

# CMD ["python3", "app.py"]