model_name='example-model'

account=$(aws sts get-caller-identity --query Account --output text)
region='us-east-1'
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${model_name}:latest"
chmod +x model/serve

aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${fullname}

docker build -t ${model_name} .
docker tag ${model_name} ${fullname}
docker push ${fullname}