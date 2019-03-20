resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "Prod-ML"
  }
}

resource "aws_subnet" "subnet_1" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.0.1.0/24"

  availability_zone="us-east-1a"
  map_public_ip_on_launch=true

  tags = {
    Name = "Prod-ML-1"
  }
}

resource "aws_subnet" "subnet_2" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "10.0.2.0/24"

  availability_zone="us-east-1b"
  map_public_ip_on_launch=true

  tags = {
    Name = "Prod-ML-2"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = "${aws_vpc.main.id}"

  tags = {
    Name = "main"
  }
}

resource "aws_route_table" "r" {
  vpc_id = "${aws_vpc.main.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.gw.id}"
  }

  tags = {
    Name = "Prod-ML"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = "${aws_subnet.subnet_1.id}"
  route_table_id = "${aws_route_table.r.id}"
}
