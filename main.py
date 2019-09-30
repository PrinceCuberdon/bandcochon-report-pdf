#!/usr/bin/env python3

import io
import logging
import os
import sys
import time

import tornado.autoreload
import tornado.ioloop
import tornado.log
import tornado.web
import weasyprint

default_format = '[%(levelname)-7s] - %(name)20s - ' \
                 '%(asctime)s - %(module)-20s: %(message)s'

logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format=default_format)

L = logging.getLogger('bandcochon-report-pdf')


class GeneratePDFHandlerMixin(object):
    @classmethod
    def is_the_body_empty(cls, body):
        if not body:
            L.error("No content given")
            return True

        return False

    @classmethod
    def generate_the_pdf_from_body(cls, body) -> bytes:
        with io.BytesIO() as content:
            weasyprint.HTML(string=body).write_pdf(content)
            return content.getvalue()


class GeneratePDFHandler(tornado.web.RequestHandler, GeneratePDFHandlerMixin):
    """
    Generate a PDF from the HTML input
    """

    def post(self):
        L.info("POST - Request a new PDF")
        if self.is_the_body_empty(self.request.body):
            self.write("Need content")
            self.set_status(400)
            return

        start = time.time()
        input_html = self.request.files['content'][0]['body']
        content = self.generate_the_pdf_from_body(input_html)

        self.set_header('Content-Type', 'application/pdf')
        self.write(content)

        duration = (time.time() - start) / 1000
        L.info("Done in %.2f sec." % duration)


def main():
    """
    Main routine
    (avoid scope pollution)
    """

    L.info("Start web service")

    app = tornado.web.Application([
        (r"/", GeneratePDFHandler),
    ])

    app.listen(address=os.environ.get('ADDRESS'),
               port=os.environ.get('PORT'))

    if os.environ.get('DEBUG') == '1':
        tornado.autoreload.start()

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
