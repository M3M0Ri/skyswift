import logging

from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the exception to the console
        logger.exception("An error occurred: " , exception)

        # Redirect to the flight:feed page
        return redirect('flight:feed')
