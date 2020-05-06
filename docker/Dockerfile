FROM gamaplatform/gama:continuous

MAINTAINER RoiArthurB <https://github.com/RoiArthurB>

#RUN git clone https://github.com/COMOKIT/CoVid19.git /usr/lib/gama/headless/comokit
RUN curl -o master.zip -fSL https://github.com/COMOKIT/COMOKIT-Model/archive/master.zip && \
	unzip master.zip -d /usr/lib/gama/headless/comokit && \
	rm master.zip && \
	# Leave root project
	mv /usr/lib/gama/headless/comokit/COMOKIT-Model-master/COMOKIT/* /usr/lib/gama/headless/comokit && \
	rm -fr /usr/lib/gama/headless/comokit/COMOKIT-Model-master

# Docker env
WORKDIR /usr/lib/gama/headless

ENTRYPOINT ["gama-headless"]
CMD ["-help"]

