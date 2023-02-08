# Start from the fredericklab base container
FROM fredericklab/basecontainer:latest

RUN pip install \
            statsmodels \
            nilearn \
            scikit-learn \
            nibabel \
            versioneer \
            pyfftw \
            numba
RUN pip install --upgrade --force-reinstall  requests

RUN df -h

# Create a shared $HOME directory
RUN useradd -m -s /bin/bash -G users capcalc
WORKDIR /home/capcalc
ENV HOME="/home/capcalc"


# Installing capcalc
COPY . /src/capcalc
RUN cd /src/capcalc && \
    python setup.py install && \
    rm -rf /src/capcalc/build /src/capcalc/dist


ENV IS_DOCKER_8395080871=1
RUN apt-get install -y --reinstall libxcb-xinerama0


RUN ldconfig
WORKDIR /tmp/
ENTRYPOINT ["/usr/local/miniconda/bin/capcalc_dispatcher"]

# set a non-root user
USER capcalc

ARG VERSION
ARG BUILD_DATE
ARG VCS_REF

RUN echo $VERSION
RUN echo $BUILD_DATE
RUN echo $VCS_REF

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="capcalc" \
      org.label-schema.description="capcalc - a set of tools for delay processing" \
      org.label-schema.url="http://nirs-fmri.net" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/bbfrederick/capcalc" \
      org.label-schema.version=$VERSION
