# Start from the fredericklab base container
FROM fredericklab/basecontainer:v0.4.0

# get build arguments
ARG BUILD_TIME
ARG BRANCH
ARG GITVERSION
ARG GITSHA
ARG GITDATE

# set and echo environment variables
ENV BUILD_TIME=$BUILD_TIME
ENV BRANCH=$BRANCH
ENV GITVERSION=${GITVERSION}
ENV GITSHA=${GITSHA}
ENV GITDATE=${GITDATE}

RUN echo "BRANCH: "$BRANCH
RUN echo "BUILD_TIME: "$BUILD_TIME
RUN echo "GITVERSION: "$GITVERSION
RUN echo "GITSHA: "$GITSHA
RUN echo "GITDATE: "$GITDATE

# copy capcalc into container
COPY . /src/capcalc
RUN echo $GITVERSION > /src/capcalc/VERSION

# init and install picachooser
RUN uv pip install --upgrade pip
RUN cd /src/capcalc && \
    uv pip install .
RUN chmod -R a+r /src/capcalc

# install versioneer
RUN cd /src/picachooser && \
    versioneer install --no-vendor && \
    rm -rf /src/picachooser/build /src/picachooser/dist

# clean up
RUN pip cache purge

# Create a shared $HOME directory
ENV USER=capcalc
RUN useradd \
    --create-home \
    --shell /bin/bash \
    --groups users \
    --home /home/$USER \
    $USER
RUN cp ~/.bashrc /home/$USER/.bashrc; chown $USER /home/$USER/.bashrc

WORKDIR /home/$USER
ENV HOME="/home/$USER"

ENV IN_DOCKER_CONTAINER=1

RUN ldconfig
WORKDIR /tmp/

# set to non-root user and initialize mamba
USER $USER
RUN /opt/miniforge3/bin/mamba init

ENTRYPOINT ["/opt/miniforge3/envs/science/bin/capcalc_dispatcher"]

LABEL org.label-schema.build-date=$BUILD_TIME \
      org.label-schema.name="capcalc" \
      org.label-schema.description="capcalc - a set of tools for delay processing" \
      org.label-schema.url="http://nirs-fmri.net" \
      org.label-schema.vcs-ref=$GITVERSION \
      org.label-schema.vcs-url="https://github.com/bbfrederick/capcalc" \
      org.label-schema.version=$GITVERSION
