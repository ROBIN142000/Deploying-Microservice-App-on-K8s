resource "aws_efs_file_system" "efs" {
    availability_zone_name = "ap-south-1a"

    encrypted = true

    lifecycle_policy {
        transition_to_ia = "AFTER_30_DAYS"
    }

    tags = {
    Name = "tasklist-efs"
  }
}

resource "aws_efs_mount_target" "efs_mount_target" {
    file_system_id = aws_efs_file_system.efs.id
    subnet_id = var.subnet_ids[0]
}

resource "aws_efs_backup_policy" "aws_efs_backup_policy" {
    file_system_id = aws_efs_file_system.efs.id

    backup_policy {
        status = "DISABLED"
  }
}