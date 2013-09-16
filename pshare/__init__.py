from . import models
from .settings import settings
from .routes import app
from .models import *

def main():
    models.open()
    app.run(
        debug = settings.debug,
        host = settings.host,
        port = settings.port,
    )
    models.close()
