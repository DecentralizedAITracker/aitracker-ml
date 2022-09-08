build: docker build . --tag aitracker-ml
tag: docker tag predictme-ml id997/aitracker-ml:0.0.3
push: docker push id997/aitracker-ml:0.3.0
hash: docker pull id997/aitracker-ml:0.3.0 | grep "Digest: sha256:" | sed 's/.*sha256:/0x/'
link: registry.hub.docker.com/id997/aitracker-ml:0.3.0


run with input_files: docker run \
    -v F:\\Projects\\iexec-aitracker\\aitracker-ml\\io\\iexec_in:/iexec_in \
    -v F:\\Projects\\iexec-aitracker\\aitracker-ml\\io\\iexec_out:/iexec_out \
    --env IEXEC_IN=/iexec_in \
    --env IEXEC_OUT=/iexec_out \
    id997/aitracker-ml:0.0.3
    