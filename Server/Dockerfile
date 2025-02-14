FROM python:3.12-slim-bookworm AS build

RUN apt-get update && apt-get install -y gcc
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 uninstall opencv-python -y
RUN pip3 install opencv-python-headless


FROM python:3.12-slim-bookworm
WORKDIR /app
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY mongodb.py . 
COPY app.py .
# COPY vgg_face_weights.h5 /root/.deepface/weights/vgg_face_weights.h5
COPY templates templates
EXPOSE 5002

CMD ["python3", "app.py"]
