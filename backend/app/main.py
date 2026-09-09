from fastapi import FastAPI

app = FastAPI(title="TIENDAJ API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
