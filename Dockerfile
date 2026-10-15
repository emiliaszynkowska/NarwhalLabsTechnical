FROM python:3.15
ENV DB_UP=false
EXPOSE 8080
ADD app.py .
ENTRYPOINT ["python", "app.py"]
