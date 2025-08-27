
FROM	ghcr.io/astral-sh/uv:python3.13-alpine
WORKDIR	/app
COPY	./pyproject.toml	.
COPY	./requirements.txt	.
COPY	.	.
COPY	.	/app
RUN	uv sync --locked
EXPOSE	8000
CMD	["uv","run","fastapi","run","src/parcelbox/main.py","--port","8000"]
