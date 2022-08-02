import boto3

rds_client = boto3.client("rds", region_name="us-east-1")
""" :type : pyboto3.rds """


RDS_DB_SUBNET_GROUP = "rds-db-subnet-group5"


def create_db_subnet_group():
    print("Creating RDS DB Subnet Group " + RDS_DB_SUBNET_GROUP)
    rds_client.create_db_subnet_group(
        DBSubnetGroupName=RDS_DB_SUBNET_GROUP,
        DBSubnetGroupDescription="My own db subnet group",
        SubnetIds=['subnet-070ee0d9f7b0e3dc1', 'subnet-078d0456146f83575', 'subnet-03b21095c200c37a6']
    )


def create_db_security_group_and_add_inbound_rule():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    """ :type : pyboto3.ec2 """

    # create security group
    security_group = ec2.create_security_group(
        GroupName="post_rds3",
        Description="RDS security group to allow public access",
        VpcId="vpc-0cb09bd4965d8af43"
    )

    # get id of the
    security_group_id = security_group['GroupId']

    print("Created RDS security group with id " + security_group_id)

    # add public access rule to sg
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 5432,
                'ToPort': 5432,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )

    print("Added inbound access rule to security group with id " + security_group_id)
    return security_group_id


def launch_rds_instance():
    print("Launching AWS RDS PostgreSQL instance...")

    security_group_id = create_db_security_group_and_add_inbound_rule()

    create_db_subnet_group()
    print("Created DB Subnet Group")

    rds_client.create_db_instance(
        DBName='proddatabase',
        DBInstanceIdentifier="pginstanceidentifier",
        DBInstanceClass="db.t3.micro",
        Engine="postgres",
        EngineVersion="13.5",
        Port=5432,
        MasterUsername="postgres",
        MasterUserPassword="holyghost123",
        AllocatedStorage=20,
        MultiAZ=False,
        StorageType="gp2",
        PubliclyAccessible=True,
        VpcSecurityGroupIds=[security_group_id],
        DBSubnetGroupName=RDS_DB_SUBNET_GROUP
    )


if __name__ == '__main__':
    launch_rds_instance()
