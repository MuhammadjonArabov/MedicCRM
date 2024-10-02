from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        new_data = {}
        for field, error_list in response.data.items():
            if isinstance(error_list, list) and len(error_list) > 0:
                new_data[field] = error_list[0]
            else:
                new_data[field] = error_list
        response.data = new_data

    return response
