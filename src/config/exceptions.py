from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


# Custom exception handler to convert Django ValidationError to DRF
# ValidationError
def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=as_serializer_error(exc))
    return exception_handler(exc, context)
