FROM python:3.13-slim
WORKDIR /app
# copy the requirements.txt first and install before copying code — this is a Docker 
# caching best practice so dependencies don't reinstall every time code is changed
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]