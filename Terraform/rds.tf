resource "aws_db_instance" "mysql-postgres-db" {
    engine = "mysql"
    db_name = "tasklist_db"
    instance_class = "db.t3.micro"
    identifier = "tasklist-db-instance"
    availability_zone = "ap-south-1c"
    multi_az = false
    storage_type = "gp2"
    allocated_storage = "20"
    port = 3306
    publicly_accessible = true
    username = "senpai"
    password = "onlysenpaiknows"
    skip_final_snapshot = true
}