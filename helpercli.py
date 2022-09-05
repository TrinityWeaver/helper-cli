import click
import boto3


class HelperCLI:
    def __init__(self):
        pass

    def aws_creds(self):
        """
        Get AWS credentials from the environment
        """
        access_key_id = click.prompt("Enter your access key id", hide_input=True)
        secret = click.prompt("Enter your secret access key", hide_input=True)
        return {"access": access_key_id, "secret": secret}

    def clientBoto3(self, creds):
        """
        Configure boto3 with AWS credentials
        """
        return boto3.client(
            "s3",
            aws_access_key_id=creds["access"],
            aws_secret_access_key=creds["secret"],
        )

    def clientResources(self, creds):
        """
        Configure boto3 with AWS credentials
        """
        return boto3.resource(
            "s3",
            aws_access_key_id=creds["access"],
            aws_secret_access_key=creds["secret"],
        )

    def get_buckets(self, client):
        """
        Get all buckets from the client
        """
        return client.list_buckets()

    def remove_buckets(self, client, buckets, s3):
        val = 2

        for bucketName in buckets["Buckets"]:
            try:
                s3_bucket = s3.Bucket(bucketName["Name"])
                bucket_versioning = s3.BucketVersioning(bucketName["Name"])
                if bucket_versioning.status == "Enabled":
                    print(f"Removing versioning from bucket {bucketName['Name']}")
                    s3_bucket.object_versions.delete()
                s3_bucket.objects.all().delete()
                print(f"Delete bucket {bucketName['Name']}")
                client.delete_bucket(Bucket=bucketName["Name"])
                print(f"Delete bucket {bucketName['Name']} successfully")
            except Exception as e:
                print(f"Error deleting bucket {bucketName['Name']}:")
                print(e)


@click.command()
@click.option(
    "-s",
    "--service",
    help="Service to use for removal resources.\nChoose one of:\n\n" + "s3",
    required=True,
)
def helper(service):
    """
    Name: helper

    Helper CLI to remove resources from AWS

    """
    helperClient = HelperCLI()
    try:
        if service == "s3":
            creds = helperClient.aws_creds()
            client = helperClient.clientBoto3(creds)
            s3 = helperClient.clientResources(creds)
            buckets = helperClient.get_buckets(client)
            helperClient.remove_buckets(client, buckets, s3)
        if service != "s3":
            print("Service not supported")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    helper()
