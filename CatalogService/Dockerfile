FROM python:3.7
COPY requirements.txt /CatalogService/requirements.txt
WORKDIR /CatalogService
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]