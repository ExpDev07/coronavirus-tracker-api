FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV VARIABLE_NAME APP

# COPY DEPENDENCIES
COPY requirements.txt ./

# COPY PROJECT
COPY ./app /app/app

# INSTALL DEPENDENCIES
RUN pip install --no-cache-dir -r  requirements.txt

EXPOSE 80
