FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# ENVS RECOMENDATIONS
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# PREPARE FOLDER
WORKDIR /api

# COPY DEPENDENCIES
COPY requirements.txt ./

# INSTALL DEPENDENCIES
RUN pip install --no-cache-dir -r  requirements.txt

# COPY PROJECT
COPY . /api/

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:APP"]