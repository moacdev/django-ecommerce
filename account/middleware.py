from django.http import JsonResponse
class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/') and not request.user.is_authenticated:
            return JsonResponse({
                "isOk": False,
                "error_type": "not-authenticated"
            })
        return self.get_response(request)
