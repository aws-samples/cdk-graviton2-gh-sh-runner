#!/bin/bash
yum update -y
# Download and build a recent version of International Components for Unicode.
# https://github.com/actions/runner/issues/629
# https://github.com/dotnet/core/blob/main/Documentation/linux-prereqs.md
# Install jq for parsing parameter store
yum install -y libicu60 jq

# Get python 3.8.x and make it the default for python3 (AL2 comes with python 3.7.x)
sudo amazon-linux-extras install -y python3.8
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Get latest runner version
VERSION_FULL=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | jq -r .tag_name)
RUNNER_VERSION="${VERSION_FULL:1}"

# Create a folder
mkdir /home/ec2-user/actions-runner && cd /home/ec2-user/actions-runner || exit
# Download the latest runner package
curl -o actions-runner-linux-arm64-${RUNNER_VERSION}.tar.gz -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-arm64-${RUNNER_VERSION}.tar.gz
# Extract the installer
tar xzf ./actions-runner-linux-arm64-${RUNNER_VERSION}.tar.gz
chown -R ec2-user /home/ec2-user/actions-runner
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/region)
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
TOKEN=$(aws ssm get-parameter --region "${REGION}" --name gh-token --with-decryption | jq -r '.Parameter.Value')
REPO=$(aws ssm get-parameter --region "${REGION}" --name gh-url | jq -r '.Parameter.Value')
sudo -i -u ec2-user bash << EOF
/home/ec2-user/actions-runner/config.sh --url "${REPO}" --token "${TOKEN}" --name gh-g2-runner-"${INSTANCE_ID}" --work /home/ec2-user/actions-runner --unattended
EOF
./svc.sh install
./svc.sh start
