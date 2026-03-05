FROM harbor.weizhipin.com/arsenal-ai/tensorrt-llm:v1.3.0rc6

ARG FILE_DIR=./maas
ARG WHEEL_NAME=truncate/tensorrt_llm-1.3.0rc7-cp312-cp312-linux_x86_64.whl

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb http://mirrors.weizhipin.com/ubuntu/ jammy main restricted universe multiverse" > /etc/apt/sources.list \
    && echo "deb http://mirrors.weizhipin.com/ubuntu/ jammy-updates main restricted universe multiverse" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.weizhipin.com/ubuntu/ jammy-security main restricted universe multiverse" >> /etc/apt/sources.list \
    && apt-get update \
    && apt install -y tzdata tmux \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.extra-index-url http://pypi-mirror.weizhipin.com/bzl-aliyun-pypi/simple && \
    pip config set global.index-url http://pypi-mirror.weizhipin.com/bzl-aliyun-pypi/simple && \
    pip config set global.index-url http://pypi-mirror.weizhipin.com/qinghua-pypi/pypi/web/simple && \
    pip config set global.trusted-host "pypi-mirror.weizhipin.com pypi-mirror.weizhipin.com" && \
    pip config set install.trusted-host "pypi-mirror.weizhipin.com pypi-mirror.weizhipin.com"


COPY ${FILE_DIR}/hack/ /
COPY ${FILE_DIR}/base-resource /opt/
RUN chmod 755 /build.sh /run.sh \
    && chmod -R 755 /opt/binary

# copy files into /app/
COPY ${FILE_DIR}/run.sh ${FILE_DIR}/pre_stop.sh ${FILE_DIR}/requirements.txt ${FILE_DIR}/register.py /app/

# copy starter
COPY ${FILE_DIR}/starter /app/starter

# Install basic requirements
RUN pip install --no-cache-dir -r /requirements.txt

# Install whls
COPY ${FILE_DIR}/whls/${WHEEL_NAME} /app/${WHEEL_NAME}
RUN pip install --no-cache-dir --no-deps --force-reinstall /app/${WHEEL_NAME} && rm /app/${WHEEL_NAME}

# ONLY for truncate mirror
COPY new2old.json /usr/local/lib/python3.12/dist-packages/

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/external:/opt/lib

WORKDIR /app

ENTRYPOINT ["sh", "/run.sh"]
