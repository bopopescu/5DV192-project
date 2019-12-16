from django.http import JsonResponse
from django.views import View as APIView


class ControllerGetBuckets(APIView):

    def get(self, request, *args, **kwargs):

        response = {
            "payload": "none",
        }

        return JsonResponse(response, safe=False, status=200)

