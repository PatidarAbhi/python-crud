# python-fast-api-poc

## Description
A CRUD based POC project using fast api.

# Steps for Deploying to AWS EC2
Log into your AWS account and create an EC2 instance using the latest stable Ubuntu Linux AM and SSH into the instance 
and run these commands to update the software repository and install our dependencies.
```bash
sudo apt-get update
sudo apt install -y python3-pip nginx
```

Optional: Set Up Nginx as a Reverse Proxy -> Add the FastAPI configuration to NGINX's folder. Create a file called fastapi_nginx .

```bash
sudo vim /etc/nginx/sites-enabled/fastapi_nginx
```

And put this config into the file (replace the IP address with your EC2 instance's public IP):
```bash
server {
    listen 80;   
    server_name <YOUR_EC2_IP>;    
    location / {        
        proxy_pass http://127.0.0.1:8000;    
    }
}
```

Start NGINX
```bash
sudo service nginx restart
```

Clone the repository
```bash
git clone https://github.com/PatidarAbhi/python-crud.git
```

Start application
```bash
cd python-crud

pip install -r requirements.txt

python -m uvicorn main:app
```

Video link for reference [click to open link](https://www.youtube.com/watch?v=SgSnz7kW-Ko)