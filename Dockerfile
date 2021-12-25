FROM python:3.10-slim as build
WORKDIR /opt

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip3 install --upgrade -r requirements.txt


FROM python:3.10-alpine
WORKDIR /opt

# これをしないとターミナルへの出力が出ない現象が起こる。
ENV PYTHONUNBUFFERED="1"
COPY --from=build /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY . .
CMD ["python3", "launcher.py"]
