import os
from os import listdir
from os.path import isfile, join
from twisted.protocols.ftp import FileExistsError

from google.cloud import storage

from app import app


class GoogleBucket:

    def __init__(self, bucket_name):
        resource_path = os.path.join(app.root_path, 'credentials.json')
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
        """
        Blobs = files
        List all files in bycjet
        :return:
        """
        bucket = self.storage_client.get_bucket(self.bucket_name)
        return bucket.list_blobs()

    def upload_file(self, file_stream, filename, content_type):

        client = self.storage_client
        bucket = client.bucket(self.bucket_name)
        blob = bucket.blob(filename)

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

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # bucket_name = "your-bucket-name"
        # source_file_name = "local/path/to/file"
        # destination_blob_name = "storage-object-name"

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    def upload_folder(self, bucket_name, source_folder, destination_folder):
        """Upload files to GCP bucket."""
        bucket = self.storage_client.bucket(bucket_name)
        files = [f for f in listdir(source_folder) if isfile(join(source_folder, f))]
        for file in files:
            local_file = source_folder + "/" + file
            blob = bucket.blob(destination_folder + "/" + file)
            blob.upload_from_filename(local_file)

    def download_blob(self, bucket_name, source_object_path, file_name, save_path):
        """Downloads a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # source_blob_name = "storage-object-name"
        # destination_file_name = "local/path/to/file"

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(source_object_path + "/" + file_name)
        blob.download_to_filename(save_path + "/" + file_name)

        print(
            "Blob {} downloaded to {}.".format(
                source_object_path, save_path
            )
        )

    def list_files_in_folder(self, bucket_name, folder_path):
        bucket = self.storage_client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=folder_path))
        return blobs

    def download_files_in_folder(self, bucket_name, folder_path, save_path):
        try:
            # Create target Directory
            os.mkdir(save_path)
            print("Directory ", save_path, " Created ")
        except FileExistsError:
            print("Error - Directory ", save_path, " already exists")
            return
        blobs = self.list_files_in_folder(bucket_name, folder_path)
        print(folder_path)
        for blob in blobs:
            file_name = blob.name.replace(folder_path, '')
            blob.download_to_filename(save_path + "/" + file_name)
