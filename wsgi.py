import logging
import sys
import warnings
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy import exc as sa_exc
from werkzeug import run_simple

from must.server import create_app

warnings.simplefilter("ignore", category=sa_exc.SAWarning)
# sentry_sdk.init(
#     SENTRY_DSN,
#     integrations=[FlaskIntegration()],
#     environment=ENVIRONMENT,
# )

app = create_app()

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    run_simple("0.0.0.0", 8888, app, use_reloader=True)
