import click
import boto3
import colored
from colored import fg, bg, attr


# Add README.md
# Add SQS Removal feature


class HelperCLI:
    def __init__(self):
        self.__access_key = None
        self.__secret_key = None
        self.__region = None
        self.__endpoint_url = None

    # Initialize helper

    def aws_creds(self) -> None:
        """
        Get AWS credentials from the environment
        """

        self.__access_key = click.prompt(
            f"{fg('163')}Enter your access key id", hide_input=True
        )
        self.__secret_key = click.prompt(
            f"{fg('163')}Enter your secret access key", hide_input=True
        )

    def clientBoto3(self, service: str) -> boto3.client:
        """
        Configure boto3 with AWS credentials
        """
        return boto3.client(
            service,
            aws_access_key_id=self.__access_key,
            aws_secret_access_key=self.__secret_key,
            region_name=self.__region,
            endpoint_url=self.__endpoint_url,
        )

    # S3 Service

    def clientResources(self) -> boto3.resource:
        """
        Configure boto3 with AWS credentials
        """
        return boto3.resource(
            "s3",
            aws_access_key_id=self.__access_key,
            aws_secret_access_key=self.__secret_key,
        )

    def get_buckets(self, client) -> dict:
        """
        Get all buckets from the client
        """
        return client.list_buckets()

    @staticmethod
    def bucket_result(deleted_buckets: str, error_buckets: str) -> None:
        print("\n\n")
        print(f"{fg(75)}Result of Operation:\n")
        print(f"{fg(10)}Buckets deleted: {deleted_buckets}\n ")
        print(f"{fg(196)}Buckets not deleted: {error_buckets}\n ")

    def remove_buckets(self, client, buckets: dict, s3) -> int:
        """
        Remove buckets
        """
        deleted_buckets = 0
        error_buckets = 0
        for bucketName in buckets["Buckets"]:
            try:
                s3_bucket = s3.Bucket(bucketName["Name"])
                bucket_versioning = s3.BucketVersioning(bucketName["Name"])
                if bucket_versioning.status == "Enabled":
                    print(
                        f"{fg(184)}Removing versioning from bucket {bucketName['Name']}"
                    )
                    s3_bucket.object_versions.delete()
                print(f"{fg(184)}Emptying bucket {bucketName['Name']}")
                s3_bucket.objects.all().delete()
                print(f"{fg(184)}Deleting bucket {bucketName['Name']}")
                client.delete_bucket(Bucket=bucketName["Name"])
                print(f"{fg(10)}Delete bucket {bucketName['Name']} successfully")
                deleted_buckets += 1
            except Exception as e:
                error_buckets += 1
                print(f"{fg(196)}Error deleting bucket {bucketName['Name']}:")
                print(e)
        return deleted_buckets, error_buckets

    # SQS Service

    def get_region(self) -> None:
        """
        Get region from the environment
        """
        self.__region = click.prompt(f"{fg('163')}Enter your region")
        self.__endpoint_url = f"https://sqs.{self.__region}.amazonaws.com"

    def list_queques(self, client) -> list:
        """
        List all queues from the client
        """
        queues = client.list_queues()
        if "QueueUrls" in queues:
            return queues
        print(f"{fg(196)}No queues found in region {self.__region} ")
        return None

    def remove_queues(self, client, queues: list) -> int:
        """
        Remove queues from the region
        """

        deleted_queues = 0
        error_queues = 0
        var = 1
        for queue in queues["QueueUrls"]:
            try:
                client.delete_queue(QueueUrl=queue)
                print(f"{fg(10)}Delete queue {queue} successfully")
                deleted_queues += 1
            except Exception as e:
                error_queues += 1
                print(f"{fg(196)}Error deleting queue {queue}:")
                print(e)
            var -= 1
            if var == 0:
                break
        return deleted_queues, error_queues

    @staticmethod
    def queue_result(deleted_queues: int, error_queues: int) -> None:
        print("\n\n")
        print(f"{fg(75)}Result of Operation:\n")
        print(f"{fg(10)}Queues deleted: {deleted_queues}\n ")
        print(f"{fg(196)}Queues not deleted: {error_queues}\n ")


@click.command()
@click.option(
    "-s",
    "--service",
    help="Service to use for removal resources\n",
    required=True,
    type=click.Choice(["s3", "sqs"]),
)
def helper(service: str) -> None:
    """
    Name: Helper

    Helper CLI to remove resources from AWS

    SYNOPSIS
          helper [options] <command>

       Use helper command help for information on a  specific  command.  Use  helper
       help  topics  to view a list of available help topics. The synopsis for
       each command shows its parameters and their usage. Optional  parameters
       are shown in square brackets.


    """
    helperClient = HelperCLI()
    try:
        if service == "s3":
            print(f"{fg(163)}Initializing S3 Service\n")
            helperClient.aws_creds()
            print("\n")
            client = helperClient.clientBoto3(service)
            s3 = helperClient.clientResources()
            buckets = helperClient.get_buckets(client)
            deleted_buckets, error_buckets = helperClient.remove_buckets(
                client, buckets, s3
            )
            helperClient.bucket_result(deleted_buckets, error_buckets)
    except Exception as e:
        print(e)

    try:
        if service == "sqs":
            print(f"{fg(163)}Initializing SQS Service\n")
            helperClient.aws_creds()
            helperClient.get_region()
            print("\n")
            client = helperClient.clientBoto3(service)
            queues = helperClient.list_queques(client)
            if queues is None:
                return
            deleted_queues, error_queues = helperClient.remove_queues(client, queues)
            helperClient.queue_result(deleted_queues, error_queues)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    helper()
