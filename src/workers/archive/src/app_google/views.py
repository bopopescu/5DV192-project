import os

from google.cloud import storage

from app import app


class GoogleBucket:

    def __init__(self, bucket_name):
        resource_path = os.path.join(app.root_path, 'Converter/credentials.json')
        self.storage_client = storage.Client.from_service_account_json(resource_path)
        self.bucket_name = bucket_name

    def create_bucket(self):
        bucket = self.storage_client.create_bucket(self.bucket_name)
        print('Bucket {} created'.format(bucket.name))

    def delete_bucket(self):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        bucket.delete()
        print('Bucket {} deleted'.format(bucket.name))

    def list_buckets(self):
        return self.storage_client.list_buckets()

    def list_buckets_names(self):
        return [bucket.name for bucket in self.storage_client.list_buckets()]

    def list_blobs(self):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        return bucket.list_blobs()

    def upload_file(self, file_stream, filename, content_type):

        client = self.storage_client
        bucket = client.bucket(self.bucket_name)
        blob = bucket.blob("uploaded/"+ filename)

        blob.upload_from_string(
            file_stream,
            content_type=content_type)

        blob.make_public()

        url = blob.public_url

        import six
        if isinstance(url, six.binary_type):
            url = url.decode('utf-8')

        return url

    def delete_blob(self, blob_name):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        return blob.delete()
