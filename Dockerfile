FROM python:alpine3.17
RUN pip install webargs
RUN pip install Flask
COPY . /app 
WORKDIR /app
RUN mkdir /app/images
CMD ["/app/entrypoint"]
