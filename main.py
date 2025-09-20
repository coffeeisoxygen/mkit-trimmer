import re

import markdown
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.custom import LoggingMiddleware
from src.custom.cst_cors import setup_cors
from src.custom.cst_exceptions import AppExceptionError
from src.custom.cst_lifespan import app_lifespan
from src.mlogg import logger
from src.router import register_routes

app = FastAPI(lifespan=app_lifespan)
# cors
setup_cors(app)
# Mask sensitive fields di logs
app.add_middleware(LoggingMiddleware, mask_fields=["password", "token", "secret"])


register_routes(app)


# Global exception handler for custom exceptions
@app.exception_handler(AppExceptionError)
async def app_exception_handler(request: Request, exc: AppExceptionError):  # noqa: ARG001, D103, RUF029
    logger.error(f"Application error: {exc.message}", extra=exc.context)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "context": exc.context},
    )


# Root endpoint
@logger.catch
@app.get("/", response_class=Response)
def read_root():
    with open("README.md", encoding="utf-8") as f:
        md_content = f.read()
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=["fenced_code"])

    # Replace mermaid code blocks with <div class="mermaid">...</div>
    def mermaid_replacer(match):
        code = match.group(1)
        return f'<div class="mermaid">{code}</div>'

    html_content = re.sub(
        r'<pre><code class="language-mermaid">([\s\S]*?)</code></pre>',
        lambda m: mermaid_replacer(m),
        html_content,
        flags=re.MULTILINE,
    )

    # Inject Mermaid.js and script to render mermaid blocks
    mermaid_script = """
<script type=\"module\">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true, theme: 'forest' });
</script>
        """
    # Wrap HTML in a basic template with custom CSS for Mermaid diagrams
    full_html = f"""
<html>
<head>
    <title>MODKIT API PARSER</title>
    <meta charset='utf-8'>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; background: #f9fafb; }}
        pre {{ background: #f4f4f4; padding: 1em; border-radius: 5px; }}
        .mermaid {{ background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); padding: 1em; margin: 2em 0; }}
        h1, h2, h3 {{ color: #2c3e50; }}
    </style>
</head>
<body>
    {html_content}
    {mermaid_script}
</body>
</html>
        """
    return Response(content=full_html, media_type="text/html")


@logger.catch
@app.get("/health")
async def health_check():
    """Health check endpoint.

    This endpoint can be used to check the health of the API.

    Returns:
        dict: A health status message.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
