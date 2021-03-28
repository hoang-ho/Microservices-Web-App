# FROM python:3.7
# COPY requirements.txt /CatalogService/requirements.txt
# WORKDIR /CatalogService
# RUN pip install -r requirements.txt
# COPY . /CatalogService
# ENTRYPOINT ["python"]
# CMD ["app.py"]

FROM python:3
ADD app/ /app
WORKDIR /app
RUN apt-get update
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"] 
CMD ["app.py"]