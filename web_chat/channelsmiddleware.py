from django.utils.deprecation import MiddlewareMixin


class CustomHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.META['HTTP_Authorization'] = "Token 0dd3ab857b93a62a55b2335712946fb193cc608f"

# def add_header_middleware(get_response):
#     def middleware(request):
#         request.META['hello'] = 'world'
#         response = get_response(request)
#         response['world'] = 'hello'
#         return response
#     return middleware