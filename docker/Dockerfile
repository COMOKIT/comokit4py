FROM gamaplatform/gama:continuous

MAINTAINER RoiArthurB <https://github.com/RoiArthurB>

# Add cURL command in docker
RUN apk add --no-cache curl

# Add COMOKIT framework
RUN curl -o master.zip -fSL https://github.com/COMOKIT/COMOKIT-Model/archive/master.zip && \
	unzip master.zip -d /comokit && \
	rm master.zip && \
	# Leave root project
	mv /comokit/COMOKIT-Model-master/COMOKIT/* /comokit && \
	rm -fr /comokit/COMOKIT-Model-master

# Add HPC scripts
RUN curl -o master.zip -fSL https://github.com/COMOKIT/COMOKIT-HPC/archive/master.zip && \
	unzip master.zip -d /comokit/hpc && \
	rm master.zip && \
	# Leave root project
	mv /comokit/hpc/COMOKIT-HPC-master/* /comokit/hpc && \
	rm -fr /comokit/hpc/COMOKIT-HPC-master

# Docker env
WORKDIR /usr/lib/gama/headless

ENTRYPOINT ["gama-headless"]
CMD ["-help"]
