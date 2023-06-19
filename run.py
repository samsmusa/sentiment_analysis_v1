import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host="localhost",
        port=7000,
        reload=True,
        access_log=True,
        log_level="debug",
        log_config='app/core/log_config.yaml'
    )
