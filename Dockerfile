# This is an auto generated Dockerfile for ros:perception
# generated from docker_images/create_ros_image.Dockerfile.em
FROM ubuntu:22.04

# Maintainer instructions has been deprecated, instead use LABEL
LABEL maintainer="tannous.geagea@wasteant.com"

# Versionining as "b-beta, a-alpha, rc - release candidate"
LABEL com.wasteant.version="1.1b1"

# [CHECK] Whether it is convenient to use the local user values or create ENV variables, or run everyhting with root
ARG user
ARG userid
ARG group
ARG groupid

# Install other necessary packages and dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -q -y --no-install-recommends \
    apt-utils \
	vim \
	git \
	iputils-ping \
	net-tools \
	netcat \
	ssh \
    curl \
    lsb-release \
    wget \
    zip \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies to build your own ROS packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -q -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3 \
    python3-pip \
	python3-wstool\
    build-essential \
	python3-pip \
	python3-distutils \
	python3-psutil \
    python3-tk \
    git \
	ffmpeg \
	&& rm -rf /var/lib/apt/lists/*

# install pip dependencies
RUN pip3 install opencv-python
RUN pip3 install numpy
RUN pip3 install pillow
RUN pip3 install imagehash
RUN pip3 install matplotlib
RUN pip3 install tqdm

# upgrade everything
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade -q -y \
   && rm -rf /var/lib/apt/lists/*

# # Set up users and groups
RUN addgroup --gid $groupid $group && \
	adduser --uid $userid --gid $groupid --disabled-password --gecos '' --shell /bin/bash $user && \
	echo "$user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$user && \
	chmod 0440 /etc/sudoers.d/$user

# # # Create initial workspace 
RUN mkdir -p /home/$user/src
RUN mkdir -p /media/$user
WORKDIR /home/$user/src

COPY . .

# Set environment variable for matplotlib (if needed for headless mode)
ENV MPLCONFIGDIR=/tmp

COPY ./entrypoint.sh /home/.
RUN /bin/bash -c "chown -R $user:$user /home/$user/"
RUN /bin/bash -c "chown -R $user:$user /media/$user"
RUN /bin/bash -c "chown $user:$user /home/entrypoint.sh"

ENTRYPOINT /bin/bash -c ". /home/entrypoint.sh"



