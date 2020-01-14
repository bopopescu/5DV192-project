FROM ubuntu:18.04
RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv
RUN apt-get install -y --no-install-recommends ffmpeg


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#Set encoding to UTF-8 - needed for bash files
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY /src /src
CMD ["python", "src/app.py"]
