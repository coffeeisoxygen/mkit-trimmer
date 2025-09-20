from app.api.debug import router as debug_router


def register_routers(app):
    app.include_router(debug_router)
