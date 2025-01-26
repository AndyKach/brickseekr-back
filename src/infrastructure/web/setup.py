from infrastructure.config.fastapi_app_config import app


@app.middleware("http")
async def add_ngrok_skip_header(request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "any value"
    return response


def setup():
    pass