<h1>Helper-CLI</h1>
<br>
```
Usage: helper [OPTIONS]
  Name: Helper
  Helper CLI to remove resources from AWS
  SYNOPSIS       helper [options] &lt;command&gt;
     Use helper command help for information on a  specific  command.  Use
     helper    help  topics  to view a list of available help topics. The
     synopsis for    each command shows its parameters and their usage.
     Optional  parameters    are shown in square brackets.
Options:
  -s, --service [s3|sqs]  Service to use for removal resources  [required]
  --help                  Show this message and exit.```
```
<h2>Overview:</h2>
<br>
<p>Easy way to empty, delete all S3 buckets and SQS queues in AWS account.</p>
<p>This tool allows quickly removing S3 buckets or SQS queues. Just run ```helper -s [s3|sqs]``` and provide credentials for the AWS user account with correct IAM permissions to allow actions on the AWS account. A script will remove automatically will remove all requested resources.</p>
<br>

<h2>Installation:</h2>
<br>
<p>Install helper-cli using pip and git:</p>
```
pip install git+https://github.com/TrinityWeaver/helper-cli.git```


