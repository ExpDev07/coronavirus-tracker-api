FROM python:3.7

# COPY DEPENDENCIES
COPY requirements.txt ./

# COPY PROJECT
COPY ./app /app

EXPOSE 80

# INSTALL DEPENDENCIES
RUN pip install --no-cache-dir -r  requirements.txt

CMD ["uvicorn", "app.main:APP", "--host", "0.0.0.0", "--port", "80"]
