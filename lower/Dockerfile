# Gunakan base image dari Amazon ECR untuk Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Set variabel lingkungan (opsional, tetapi bisa membantu)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Salin requirements.txt dan instal dependensi
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Salin kode sumber ke direktori kerja Lambda
COPY . ${LAMBDA_TASK_ROOT}

# Set perintah default untuk Lambda untuk memanggil handler Anda
CMD [ "main.handler" ]
