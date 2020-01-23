FROM ubuntu:18.04
RUN apt-get update && \
apt-get install -y --no-install-recommends python3 python3-virtualenv && \
apt-get -y install wget unzip && \
wget https://releases.hashicorp.com/terraform/0.12.19/terraform_0.12.19_linux_amd64.zip && \
unzip terraform_0.12.19_linux_amd64.zip && \
mv terraform /usr/local/bin/


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#Set encoding to UTF-8 - needed for bash files
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Run the application:
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "src/app.py"]
