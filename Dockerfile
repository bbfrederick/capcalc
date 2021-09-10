# Use Ubuntu 20.04 LTS
FROM ubuntu:20.04

# Prepare environment
RUN df -h
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
                    curl \
                    bzip2 \
                    ca-certificates \
                    xvfb \
                    build-essential \
                    autoconf \
                    libtool \
                    gnupg \
                    pkg-config \
                    xterm \
                    libgl1-mesa-glx \
                    libx11-xcb1 \
                    lsb-release \
                    git
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York
RUN apt-get install -y tzdata
RUN apt-get install -y --reinstall libqt5dbus5 
RUN apt-get install -y --reinstall libqt5widgets5 
RUN apt-get install -y --reinstall libqt5network5 
RUN apt-get remove qtchooser
RUN apt-get install -y --reinstall libqt5gui5 
RUN apt-get install -y --reinstall libqt5core5a 
RUN apt-get install -y --reinstall libxkbcommon-x11-0
RUN apt-get install -y --reinstall libxcb-xinerama0


RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Installing and setting up miniconda
RUN curl -sSLO https://repo.continuum.io/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh && \
    bash Miniconda3-4.7.12.1-Linux-x86_64.sh -b -p /usr/local/miniconda && \
    rm Miniconda3-4.7.12.1-Linux-x86_64.sh


# Set CPATH for packages relying on compiled libs (e.g. indexed_gzip)
ENV PATH="/usr/local/miniconda/bin:$PATH" \
    CPATH="/usr/local/miniconda/include/:$CPATH" \
    LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    PYTHONNOUSERSITE=1


# Update to the newest version of conda
RUN conda config --add channels conda-forge
RUN conda update -n base -c defaults conda


# Install mamba so we can install packages before the heat death of the universe
RUN conda install -y mamba
RUN conda clean --all


# Installing precomputed python packages
RUN mamba install -y python=3.9.6 \
                     pip \
                     scipy \
                     numpy \
                     matplotlib \
                     mkl \
                     mkl-service \
                     statsmodels \
                     scikit-image \
                     scikit-learn \
                     nibabel \
                     nilearn \
                     keras \
                     h5py \
                     "tensorflow>=2.4.0" \
                     pyqtgraph \
                     pyfftw \
                     pandas \
                     versioneer \
                     numba; sync && \
    chmod -R a+rX /usr/local/miniconda; sync && \
    chmod +x /usr/local/miniconda/bin/*; sync && \
    conda build purge-all; sync && \
    conda clean -tipsy && sync
RUN df -h


# Create a shared $HOME directory
RUN useradd -m -s /bin/bash -G users capcalc
WORKDIR /home/capcalc
ENV HOME="/home/capcalc"


# Precaching fonts, set 'Agg' as default backend for matplotlib
RUN python -c "from matplotlib import font_manager" && \
    sed -i 's/\(backend *: \).*$/\1Agg/g' $( python -c "import matplotlib; print(matplotlib.matplotlib_fname())" )


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
