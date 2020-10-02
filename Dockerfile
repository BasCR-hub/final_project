FROM python:3.7-slim
WORKDIR ./app
EXPOSE 8501
COPY . .
RUN apt-get update
RUN apt-get -y install curl
RUN apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev -y
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit","run"]
CMD ["app.py"]