FROM python:3.8
ADD ./ /code
WORKDIR code
ENV FLASK_APP=app.py
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]