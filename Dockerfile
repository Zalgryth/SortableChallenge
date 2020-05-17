FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY auction auction
CMD ["python", "-m", "auction.main"]
