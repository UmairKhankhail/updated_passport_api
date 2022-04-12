FROM ubuntu
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install tesseract-ocr

COPY . /usr/app/
EXPOSE 80
WORKDIR /usr/app/
RUN pip install pytesseract
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
CMD ["uvicorn", "passport_api:app", "--host", "0.0.0.0", "--port", "80"]
 