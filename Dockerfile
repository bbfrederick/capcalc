# Start from the fredericklab base container
FROM fredericklab/basecontainer:latest

# Installing precomputed python packages
RUN mamba install -y statsmodels \
                     pandas \
                     scikit-image \
                     scikit-learn=0.23.2 \
                     nilearn
RUN mamba install -y nibabel \
                     h5py \
                     pyqtgraph \
                     pyfftw
RUN mamba install -y versioneer \
                     numba
RUN mamba install -y keras \
                     tensorflow
RUN chmod -R a+rX /usr/local/miniconda
RUN chmod +x /usr/local/miniconda/bin/*
RUN conda-build purge-all
RUN mamba clean -y --all


RUN df -h

# Create a shared $HOME directory
RUN useradd -m -s /bin/bash -G users capcalc
WORKDIR /home/capcalc
ENV HOME="/home/capcalc"


# Installing capcalc
COPY . /src/capcalc
RUN pip install rapidtide
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
