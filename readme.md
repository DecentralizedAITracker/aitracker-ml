build: docker build . --tag aitracker-ml-rlcusdt
tag: docker tag aitracker-ml-xmrusdt id997/aitracker-ml-rlcusdt:1.0.0
push: docker push id997/aitracker-ml-rlcusdt:1.0.0
hash: docker pull id997/aitracker-ml-rlcusdt:1.0.0 | grep "Digest: sha256:" | sed 's/.*sha256:/0x/'
link: registry.hub.docker.com/id997/aitracker-ml-btcusdt:0.1.3

link: registry.hub.docker.com/id997/aitracker-ml-btcusdt:0.1.3
link: registry.hub.docker.com/id997/aitracker-ml-xmrusdt:1.0.0
link: registry.hub.docker.com/id997/aitracker-ml-rlcusdt:1.0.0

run with input_files: docker run \
    -v /home/id/Projects/iexec-aitracker/aitracker-ml/io/iexec_in:/iexec_in \
    -v /home/id/Projects/iexec-aitracker/aitracker-ml/io/iexec_out:/iexec_out \
    -e IEXEC_IN=/iexec_in \
    -e IEXEC_OUT=/iexec_out \
    -e IEXEC_INPUT_FILE_NAME_1=public_key_web.pem \
    -e IEXEC_INPUT_FILES_NUMBER=1 \
    aitracker-ml-btcusdt

    run with input_files: docker run \
    -v /home/id/Projects/iexec-aitracker/aitracker-ml/io/iexec_in:/iexec_in \
    -v /home/id/Projects/iexec-aitracker/aitracker-ml/io/iexec_out:/iexec_out \
    -e IEXEC_IN=/iexec_in \
    -e IEXEC_OUT=/iexec_out \
    aitracker-ml-btcusdt