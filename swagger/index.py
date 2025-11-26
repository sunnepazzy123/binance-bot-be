from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="DarkMind API",
        version="1.0.0",
        description="""DarkMind Bot API is a comprehensive trading automation platform designed for cryptocurrency markets. 
        It provides secure endpoints for:

        - **User Management**: Register, login, and manage account information securely.
        - **Trading Operations**: Submit buy/sell orders, monitor trade history, and manage positions.
        - **Market Data**: Retrieve real-time price streams and symbol configurations.
        - **Risk Management**: Configure stop-loss, take-profit, and volatility thresholds.
        - **Authentication**: All endpoints are secured with JWT Bearer tokens; cookies are optionally supported.

        The API is intended for programmatic access by trading bots and web clients. 
        Ensure your JWT tokens are kept secure and that HTTPS is used in production environments.""",
        routes=app.routes,
    )

    # Ensure 'components' exists
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema
