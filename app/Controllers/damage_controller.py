from pathlib import Path
from typing import cast

from fastapi import Body, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.Controllers.environment import Config

from app.Controllers.Models.calculate_hit import CalculateHitInput
from app.Controllers.Models.calculate_hit import CalculateHitOutput
from app.Controllers.Services.calculate_hit_service import calculate_hit_damage


CSS_PATH = Path(__file__).with_name("damage_controller.css")
OPENAPI_URL = "/openapi.json"


app = FastAPI(
    title="Damage Controller",
    description="Small API for damage tooling and local testing.",
    version="1.0.0",
    openapi_url=OPENAPI_URL,
    docs_url=None,
    redoc_url=None,
)


@app.get("/test", response_class=PlainTextResponse)
def test() -> str:
    return "hello world"


@app.post("/calculate_hit", response_model=CalculateHitOutput)
def calculate_hit(
    payload: CalculateHitInput = Body(
        ...,
        openapi_examples={
            "default": {
                "summary": "Tbow Maiden",
                "value": {
                    "Weapon": "Twisted Bow",
                    "Monster": {
                        "Name": "Maiden",
                        "ReduceDefense": True,
                        "Defense": 80,
                    },
                    "Scale": 3,
                },
            }
        },
    ),
) -> CalculateHitOutput:
    try:
        damage, monster_defense = calculate_hit_damage(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CalculateHitOutput(damage=damage, monster_defense=monster_defense)


if not Config.is_prod:

    @app.get("/docs", include_in_schema=False)
    def docs() -> HTMLResponse:
        openapi_url = cast(str, app.openapi_url)
        html = get_swagger_ui_html(
            openapi_url=openapi_url,
            title=f"{app.title} - Swagger UI",
            swagger_ui_parameters={"tryItOutEnabled": True},
        )
        dark_css = CSS_PATH.read_text(encoding="utf-8")
        style_tag = f"<style>{dark_css}</style>"
        body = html.body or b""
        content = body.decode("utf-8").replace("</head>", f"{style_tag}</head>")
        return HTMLResponse(content=content)
