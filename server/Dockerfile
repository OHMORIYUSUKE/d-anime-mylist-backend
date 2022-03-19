FROM python:3.8

# 必要なツール(スクレイピング)をインストール
RUN apt-get update && apt-get install -y unzip wget vim
# google-chrome 
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
wget http://dl.google.com/linux/deb/pool/main/g/google-chrome-unstable/google-chrome-unstable_93.0.4577.18-1_amd64.deb && \
apt-get install -y -f ./google-chrome-unstable_93.0.4577.18-1_amd64.deb
# ChromeDriver 
ADD https://chromedriver.storage.googleapis.com/93.0.4577.15/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
unzip chromedriver_linux64.zip
# path
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome

# コンテナ内で必要なパッケージをインストール
WORKDIR /app
COPY /app .
RUN pip install -r requirements.txt

EXPOSE 8000
# FastAPIを8000ポートで待機
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]