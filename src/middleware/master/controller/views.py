from django.http import JsonResponse
from django.views import View as APIView

from controller.includes.google_bucket import GoogleBucket
from server.settings import GS_BUCKET_NAME


class ControllerGetBuckets(APIView):

    def get(self, request, *args, **kwargs):

        bucket = GoogleBucket(GS_BUCKET_NAME)
        print(bucket.list_buckets_names())

        blobs = bucket.list_blobs()

        for blob in blobs:
            print(blob.name)

        response = {
            "payload": "none",
        }

        return JsonResponse(response, safe=False, status=200)

