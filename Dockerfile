#See specific build arguments within each section
# USERNAME
# CONDA_BASE_ENV
# CONDA_CREATE_ENV1

FROM nvcr.io/nvidia/cuda:11.2.1-cudnn8-runtime-ubuntu18.04

RUN apt-get update && apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gcc \ 
  gnupg \
  makepasswd \
  software-properties-common \
  sudo \
  unzip \
  wget 

#Install GitHub command line interface tools
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0 && \
  add-apt-repository https://cli.github.com/packages && \
  apt-get update && apt-get install -y gh  

#Install MSFT Azure command line interface tools
#RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

#Install Amazon Web Services command line interface tools
#RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip" && \ 
#  unzip awscliv2.zip && \
#  ./aws/install && \ 
#  rm -r aws && \
#  rm awscliv2.zip

#Install Google Cloud Platform command line interface tools
#RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
#  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && \ 
#  apt-get update && apt-get install -y google-cloud-sdk
     
#Install Micro editor
RUN curl https://getmic.ro | bash && \
  mv micro /usr/bin && \
  apt-get update && apt-get install -y \
  xclip \
  xsel 

#Configure users and groups
ARG USERNAME=jaseidel
ARG CONDA_GROUP=conda_users
ARG CONDA_PATH=/usr/local/miniconda3
RUN --mount=type=secret,dst=/userpasswd,id=userpasswd \
  groupadd ${CONDA_GROUP} && \
  useradd -ms /bin/bash -p $(makepasswd --crypt --clearfrom /userpasswd | awk '{print $2}') ${USERNAME} && \
  usermod -a -G ${CONDA_GROUP} ${USERNAME} && \
  usermod -a -G sudo ${USERNAME} && \
  mkdir ${CONDA_PATH} && \
  chgrp ${CONDA_GROUP} ${CONDA_PATH} && \
  chmod 775 ${CONDA_PATH}

#Install MiniConda with conda user group permissions
USER ${USERNAME}
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output /home/${USERNAME}/Miniconda3-latest-Linux-x86_64.sh && \
  bash /home/${USERNAME}/Miniconda3-latest-Linux-x86_64.sh -b -u -p ${CONDA_PATH} && \
  rm /home/${USERNAME}/Miniconda3-latest-Linux-x86_64.sh && \
  bash && ${CONDA_PATH}/bin/conda init

#Configure Conda Environments - be sure files end with conda_env.yml
COPY ./conda_envs/*conda_env.yml /home/${USERNAME}/envs/
ARG CONDA_BASE_ENV=base_conda_env.yml
ARG CONDA_CREATE_ENV1=mitx_conda_env.yml

#RUN ${CONDA_PATH}/bin/conda env create --file /home/${USERNAME}/envs/${CONDA_CREATE_ENV1} 
RUN ${CONDA_PATH}/bin/conda env update --name base --file /home/${USERNAME}/envs/${CONDA_BASE_ENV}

#Starting directory
WORKDIR /home/${USERNAME}


#START MOUNTING CLOUD VOLUMES NEXT

#gh auth login
#az login
#gcloud init

