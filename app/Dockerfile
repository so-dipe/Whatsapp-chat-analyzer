FROM python:3.10.4

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD streamlit run  main.py  --server.enableCORS false --server.enableXsrfProtection false