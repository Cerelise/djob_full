from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # 首先调用REST framework默认的异常处理，
    # 以获得标准的错误响应。
    # exc 错误原因  context 错误信息

    response = exception_handler(exc, context)

    # 接下来将HTTP状态码加到响应中。
    if response is not None:
   
        response.data['status_code'] = response.status_code
 
    return response