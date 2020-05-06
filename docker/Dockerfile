FROM gamaplatform/gama:continuous

MAINTAINER RoiArthurB <https://github.com/RoiArthurB>

# Add COMOKIT framework
RUN curl -o master.zip -fSL https://github.com/COMOKIT/COMOKIT-Model/archive/master.zip && \
	unzip master.zip -d /usr/lib/gama/headless/comokit && \
	rm master.zip && \
	# Leave root project
	mv /usr/lib/gama/headless/comokit/COMOKIT-Model-master/COMOKIT/* /usr/lib/gama/headless/comokit && \
	rm -fr /usr/lib/gama/headless/comokit/COMOKIT-Model-master

# Add HPC scripts
RUN curl -o master.zip -fSL https://github.com/COMOKIT/COMOKIT-HPC/archive/master.zip && \
	unzip master.zip -d /usr/lib/gama/headless/hpc && \
	rm master.zip && \
	# Leave root project
	mv /usr/lib/gama/headless/hpc/COMOKIT-HPC-master/scripts/* /usr/lib/gama/headless/hpc && \
	rm -fr /usr/lib/gama/headless/hpc/COMOKIT-HPC-master

# Docker env
WORKDIR /usr/lib/gama/headless

ENTRYPOINT ["gama-headless"]
CMD ["-help"]

