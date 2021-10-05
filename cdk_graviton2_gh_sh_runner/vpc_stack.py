from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class VPCStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, cidr: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self, "GHRunnerBlogVPC",
            # Cast as string to be safe.
            cidr=str(cidr),
            max_azs=2
        )

        core.CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
