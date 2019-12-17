from django.http import JsonResponse
from django.views import View as APIView

from controller.includes.google_bucket import GoogleBucket
from server.settings import GS_BUCKET_NAME


class ControllerGetBuckets(APIView):

    def get(self, request, *args, **kwargs):

        controller_get_bucket_files = ControllerGetBucketFiles()

        for blob in controller_get_bucket_files.get_files('uploaded'):
            print(blob.name)

        for blob in controller_get_bucket_files.get_files('split'):
            print(blob.name)

        for blob in controller_get_bucket_files.get_files('transcoded'):
            print(blob.name)

        for blob in controller_get_bucket_files.get_files('merged'):
            print(blob.name)

        status = 200
        response = {"status": status}
        return JsonResponse(response, safe=False, status=status)


class ControllerGetBucketFiles:

    def get_files(self, prefix):
        bucket = GoogleBucket(GS_BUCKET_NAME)
        return bucket.storage_client.list_blobs(GS_BUCKET_NAME, prefix=prefix, delimiter=prefix+"/")


