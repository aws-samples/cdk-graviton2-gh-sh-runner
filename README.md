# Building ARM64 Applications on AWS Graviton2 using the AWS CDK and Self-Hosted Runners for GitHub Actions

## Stack Components
 * __./app.py__ - The main entry point to the stack requires the $VPC_CIDR environment variable to be set.
 * __cdk_graviton2_gh_sh_runner/vpc_stack.py__ – Defines a Virtual Private Cloud (VPC) across two Availability Zones with an IPv4 CIDR block that you set via $VPC_CIDR. A NAT gateway will be created in each public subnet for egress traffic through the VPC’s internet gateway. The private subnet contains the EC2 instance for the self-hosted runner.
 * __cdk_graviton2_gh_sh_runner/ec2_stack.py__ – This defines our AMI, the instance type, and configuration. We’ll use Amazon Linux 2 for the operating system on the runner instance. We also create an IAM role, and add the `AmazonSSMManagedInstanceCore` policy.

## Prerequisites
The following steps are based on these instructions for [Adding self-hosted runners - GitHub Docs](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners#adding-a-self-hosted-runner-to-an-organization).
1. Navigate to the GitHub organization where you'd like to configure a custom GitHub Action Runner.
2. Under your organization, click *Settings*.
3. In the left sidebar, click *Actions*, then click *Runners*.
4. Under "Runners", click *Add runner*.
5. Copy the token value under the "Configure" section.

NOTE: this is an automatically-generated time-limited token to authenticate the request.

Next, launch an AWS CloudShell environment, and create the following AWS SSM Parameter Store values in the AWS account where you'll be deploying the AWS CDK stack. The names `gh-url` and `gh-token`, and types `String` and `SecureString`, respectively, are required for this integration:

```bash
aws ssm put-parameter --name gh-token --type SecureString --value ABCDEFGHIJKLMNOPQRSTUVWXYZABC
aws ssm put-parameter --name gh-url --type String --value https://github.com/your/repository
```

## Installation and Deployment
[AWS CloudShell](https://aws.amazon.com/cloudshell/) is the preferred environment for installation and deployment.
```bash
sudo npm install aws-cdk -g
git clone https://github.com/aws-samples/cdk-graviton2-gh-sh-runner.git
cd cdk-graviton2-gh-sh-runner
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export VPC_CIDR="192.168.0.0/24" # Set your CIDR here.
export AWS_ACCOUNT=`aws sts get-caller-identity | jq -r '.Account'`
cdk bootstrap aws://$AWS_ACCOUNT/$AWS_REGION
cdk deploy --all
# Note: Before the EC2 stack deploys you will be prompted for approval
# The message states 'This deployment will make potentially sensitive changes according to your current security approval level (--require-approval broadening).' and prompts for y/n
```
These steps will deploy an EC2 instance self-hosted runner that is added to your GitHub organization (as specified by the gh-url parameter in the prerequisites).

You can confirm the self-hosted runner has been successfully added to your organization by navigating to the Settings tab for your GitHub organization, selecting the Actions options from the left-hand panel, then selecting Runners.

## Troubleshooting
Refer to the instance ID outputted as part of the CDK stack, then use one of the following steps to get console output for the instance: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-console.html#instance-console-console-output
Scroll to the GitHub Actions self-hosted runner registration output.

Common issues include:
* The provided GitHub token is not authorized for the provided GitHub URL.
* The provided GitHub URL is incorrect.
* There is a typo in one of the parameter store values.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
