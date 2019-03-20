variable "cluster-name" {
  default = "prod-ml"
  type    = "string"
}

resource "aws_eks_cluster" "prod-ml" {
  name     = "prod-ml"
  role_arn = "${aws_iam_role.prod-ml.arn}"

  vpc_config {
    subnet_ids = ["${aws_subnet.subnet_1.id}", "${aws_subnet.subnet_2.id}"]
  }
}

output "endpoint" {
  value = "${aws_eks_cluster.prod-ml.endpoint}"
}

output "kubeconfig-certificate-authority-data" {
  value = "${aws_eks_cluster.prod-ml.certificate_authority.0.data}"
}

resource "aws_iam_role" "prod-ml" {
  name = "prod-ml-eks-cluster"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "prod-ml-eks-cluster-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = "${aws_iam_role.prod-ml.name}"
}

resource "aws_iam_role_policy_attachment" "prod-ml-eks-cluster-AmazonEKSServicePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = "${aws_iam_role.prod-ml.name}"
}

## ControlPlaneSecurityGroup
resource "aws_security_group" "prod-ml-eks-cluster" {
  name        = "prod-ml-eks-cluster"
  description = "Allow all inbound traffic"
  vpc_id      = "${aws_vpc.main.id}"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

locals {
  config_map_aws_auth = <<CONFIGMAPAWSAUTH


apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: ${aws_iam_role.prod-ml-eks-node.arn}
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
CONFIGMAPAWSAUTH
}

output "config_map_aws_auth" {
  value = "${local.config_map_aws_auth}"
}
