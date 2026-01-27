FROM ghcr.io/astral-sh/uv:python3.14-alpine
WORKDIR /plankapy
ADD . /plankapy
RUN uv build
RUN pip install .