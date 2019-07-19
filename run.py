import argparse

import set_logging
from app import app
import srvconf

set_logging.set_logging()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='my severless,a very awesome project')
    parser.add_argument('-p', action="store", default=8000,
                        help='input the port which site runs')
    parser.add_argument('-d', action="store", default=True,
                        help='debug options, set True or False')
    results = parser.parse_args()

    srvconf.port = int(results.p)

    app.run(host="0.0.0.0", port=results.p, debug=results.d, workers=1)
