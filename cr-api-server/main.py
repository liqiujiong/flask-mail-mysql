# -*- coding:utf-8 -*-

from cr_api_server import app
from cr_api_server.config import Config


def main():
    app.run(host="0.0.0.0", port=Config.PORT)


if __name__ == "__main__":
    main()
