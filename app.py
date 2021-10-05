#!/usr/bin/env python3
import os
import sys

from aws_cdk import core

from cdk_graviton2_gh_sh_runner.ec2_stack import EC2Stack
from cdk_graviton2_gh_sh_runner.vpc_stack import VPCStack

# To be injected at synth/deployment time
CIDR = os.getenv("VPC_CIDR", "")

if not CIDR:
    print("Please set the VPC_CIDR environment variable before execution.")
    sys.exit(1)

app = core.App()

net = VPCStack(app, "GHRunnerBlog-VPCStack", CIDR)
ec2 = EC2Stack(app, "GHRunnerBlog-EC2Stack", net.vpc)

ec2.add_dependency(net)

app.synth()
