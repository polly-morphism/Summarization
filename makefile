install:
	@sudo apt update
	@sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
	@curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	@sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
	@curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
	@curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu16.04/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
	@sudo apt update
	@sudo apt install -y docker-ce docker-compose
	@sudo apt install -y nvidia-docker2
	@sudo apt update
	@sudo apt autoremove -y
	@sudo pkill -SIGHUP dockerd
	@docker volume create --name=nvidia_driver
build:
	@cp ./requirements.txt ./services/summarization/requirements.txt
	@docker-compose build
	@rm ./services/summarization/requirements.txt
run:
	@docker-compose up -d
stop:
	@docker-compose down
clean:
	@docker image prune
	@docker container prune
	@docker network prune

