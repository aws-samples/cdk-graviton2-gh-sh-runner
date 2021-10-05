from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core
)

with open('./cdk_graviton2_gh_sh_runner/user_data/userdata.sh') as f:
    USER_DATA = f.read()


class EC2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Latest Amazon Linux 2 AMI for ARM
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            cpu_type=ec2.AmazonLinuxCpuType.ARM_64)

        # Role for SSM
        role = iam.Role(self, "InstanceSSM",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            "AmazonSSMManagedInstanceCore"))

        # Instance Type is a t4g.large with 128GB of EBS Storage, substitute more power/storage as appropriate.
        self.instance = ec2.Instance(
            self,
            "GHRunnerInstance",
            instance_type=ec2.InstanceType("t4g.large"),
            machine_image=amzn_linux,
            block_devices=[ec2.BlockDevice(
                device_name="/dev/xvda",
                volume=ec2.BlockDeviceVolume.ebs(
                    volume_size=128)
            )],
            vpc=vpc,
            role=role,
            user_data=ec2.UserData.custom(USER_DATA)
        )

        core.CfnOutput(self, "Output",
                       value=self.instance.instance_id)
