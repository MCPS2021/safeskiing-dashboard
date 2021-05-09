FROM python:3.7.0-stretch
ADD ./ /code
WORKDIR code
ENV FLASK_APP=app.py
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]