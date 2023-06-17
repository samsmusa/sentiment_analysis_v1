import requests


# documentation:https://fastapi.tiangolo.com/advanced/extending-openapi/

def downlaod_ui():
    swagger_ui = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js'
    swagger_css = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css'
    redoc_ui = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'
    swagger_ui = requests.get(swagger_ui, allow_redirects=True)
    swagger_css = requests.get(swagger_css, allow_redirects=True)
    redoc_ui = requests.get(redoc_ui, allow_redirects=True)

    open('swagger-ui-bundle.js', 'wb').write(swagger_ui.content)
    open('swagger-ui.css', 'wb').write(swagger_css.content)
    open('redoc.standalone.js', 'wb').write(redoc_ui.content)