FROM gamaplatform/gama:continuous

MAINTAINER RoiArthurB <https://github.com/RoiArthurB>

# Add cURL command in docker
RUN apk add --no-cache curl python py3-numpy

# Add COMOKIT framework
RUN curl -o master.zip -fSLq https://github.com/COMOKIT/COMOKIT-Model/archive/master.zip && \
	mkdir -p /comokit/hpc && \
	unzip master.zip -d /comokit && \
	rm master.zip && \
	# Leave root project
	mv /comokit/COMOKIT-Model-master/COMOKIT/* /comokit && \
	mv /comokit/COMOKIT-Model-master/COMOKIT/.project /comokit/.project && \
	rm -fr /comokit/COMOKIT-Model-master && \
	# Add HPC scripts
	curl -o master.zip -fSLq https://github.com/COMOKIT/COMOKIT-HPC/archive/master.zip && \
	unzip master.zip -d /comokit/hpc && \
	rm master.zip && \
	# Leave root project
	mv /comokit/hpc/COMOKIT-HPC-master/* /comokit/hpc && \
	rm -fr /comokit/hpc/COMOKIT-HPC-master && \
	# Make all scripts executable
	find /comokit/hpc -type f -exec chmod +x {} \;

# Docker env
WORKDIR /usr/lib/gama/headless

ENTRYPOINT ["gama-headless"]
CMD ["-help"]
