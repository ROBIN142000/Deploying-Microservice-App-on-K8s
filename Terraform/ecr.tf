resource "aws_ecr_repository" "backend_ecr" {
  name = "backend"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "auth_ecr" {
  name = "auth"
  image_tag_mutability = "MUTABLE"
}