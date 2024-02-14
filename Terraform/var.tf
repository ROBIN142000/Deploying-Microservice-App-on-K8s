variable "ap-south-1a_subnetID" {
    default = [ "ap-south-1a ID" ]
}

variable "cluster_name" {
  default = "Tasklist"
}

variable "eks_role_arn" {
  default = "your eks role arn"
}

variable "kubernetes_version" {
  default = "1.28"
}

variable "subnet_ids" {
  default = [ "ap-south-1a ID", "ap-south-1b ID", "ap-south-1c ID" ]
}

variable "node_role_arn" {
  default = "your node role arn"
}