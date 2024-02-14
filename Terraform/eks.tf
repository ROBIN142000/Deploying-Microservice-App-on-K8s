resource "aws_eks_cluster" "tasklist_cluster" {
  name = var.cluster_name
  role_arn = var.eks_role_arn
  version = var.kubernetes_version

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

resource "aws_eks_node_group" "backend-ng" {
  cluster_name = aws_eks_cluster.tasklist_cluster.name
  node_group_name = "backend-nodeGroup"
  node_role_arn = var.node_role_arn
  subnet_ids = var.ap-south-1a_subnetID

  instance_types = ["t3.small"]

  scaling_config {
    desired_size = 1
    max_size = 4
    min_size = 1
  }

  update_config {
    max_unavailable = 1
  }

  labels = {
    "node-group" = "backend-ng"
  }
}

resource "aws_eks_node_group" "auth-ng" {
  cluster_name = aws_eks_cluster.tasklist_cluster.name
  node_group_name = "auth-nodeGroup"
  node_role_arn = var.node_role_arn
  subnet_ids = var.subnet_ids

  instance_types = ["t3.small"]

  scaling_config {
    desired_size = 1
    max_size = 4
    min_size = 1
  }

  update_config {
    max_unavailable = 1
  }

  labels = {
    "node-group" = "auth-ng"
  }
}

// efs csi driver is dependent on node so unless you have provisioned node do not add the add-on.
// also efs csi depends on the ip address, if the node does not have an ip address to give to efs
// csi driver, the add-on will get degraded. Make sure the eni has an additional ip address to give to the add-on
// The nodes I have used here has sufficient ip addesses.

resource "aws_eks_addon" "efs_csi_driver" {
  cluster_name = var.cluster_name
  addon_name = "aws-efs-csi-driver"
  depends_on = [ 
    aws_eks_node_group.backend-ng
   ]
   service_account_role_arn = aws_iam_role.csi_driver_role.arn
}

data "tls_certificate" "eks" {
  url = aws_eks_cluster.tasklist_cluster.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "cluster_oidc_provider" {
  depends_on = [ aws_eks_cluster.tasklist_cluster ]
  client_id_list     = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url = aws_eks_cluster.tasklist_cluster.identity[0].oidc[0].issuer
}

resource "aws_iam_role" "csi_driver_role" {
  name = "AmazonEKS_EFS_CSI_DriverRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy"
  role = aws_iam_role.csi_driver_role.name
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Federated"
      identifiers = ["${aws_iam_openid_connect_provider.cluster_oidc_provider.arn}"]
    }

    condition {
      test = "StringLike"
      variable = "${aws_iam_openid_connect_provider.cluster_oidc_provider.url}:aud"
      values = ["sts.amazonaws.com"]
    }

    condition {
      test = "StringLike"
      variable = "${aws_iam_openid_connect_provider.cluster_oidc_provider.url}:sub"
      values = ["system:serviceaccount:kube-system:efs-csi-*"]
    }

    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]
  }
}