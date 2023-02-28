from loguru import logger

from app import create_app


app = create_app()


if __name__ == '__main__':
    try:
        app.run()
    except (SystemError, KeyboardInterrupt, EOFError) as ex:
        logger.warning(ex)
    finally:
        logger.info('Applicaton stopped!')