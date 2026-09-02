#!/bin/bash

dnf update -y

# Install Docker
dnf install -y docker

# Start Docker
systemctl enable docker
systemctl start docker

# Allow ec2-user to run Docker
usermod -aG docker ec2-user

# Install nginx
dnf install -y nginx

# Start nginx
systemctl enable nginx
systemctl start nginx

# Simple test page
cat > /usr/share/nginx/html/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Luxe Store</title>
</head>
<body>
    <h1>Luxe Store</h1>
    <p>Terraform + AWS + EC2 + User Data</p>
    <p>Docker and Nginx are installed.</p>
</body>
</html>
EOF