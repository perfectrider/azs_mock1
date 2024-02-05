FROM python:3.11

WORKDIR /app

RUN git clone -b $CODE_BRANCH https://github.com/perfectrider/azs_mock1.git .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["uvicorn main:app --reload"]

