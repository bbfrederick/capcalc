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

# init and install capcalc
RUN uv pip install --upgrade pip
RUN cd /src/capcalc && \
    uv pip install .
RUN chmod -R a+r /src/capcalc

# install versioneer
RUN cd /src/capcalc && \
    versioneer install --no-vendor && \
    rm -rf /src/capcalc/build /src/capcalc/dist

# update the paths to libraries
RUN ldconfig

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
RUN chown -R $USER /src/$USER
WORKDIR /home/$USER
ENV HOME="/home/$USER"

RUN /opt/miniforge3/bin/mamba init
RUN echo "mamba activate science" >> /home/capcalc/.bashrc
RUN echo "/opt/miniforge3/bin/mamba activate science" >> /home/capcalc/.bashrc

# switch to the capcalc user
USER $USER

# set up variable for non-interactive shell
ENV PATH=/opt/miniforge3/envs/science/bin:/opt/miniforge3/condabin:.:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

ENV IN_DOCKER_CONTAINER=1

WORKDIR /tmp/

# set to non-root user and initialize mamba
USER $USER
RUN /opt/miniforge3/bin/mamba init

ENTRYPOINT ["/opt/miniforge3/envs/science/bin/capcalc_dispatcher"]

LABEL org.label-schema.build-date=$BUILD_TIME \
      org.label-schema.name="capcalc" \
      org.label-schema.description="capcalc - coactivation pattern analysis software" \
      org.label-schema.url="http://nirs-fmri.net" \
      org.label-schema.vcs-ref=$GITVERSION \
      org.label-schema.vcs-url="https://github.com/bbfrederick/capcalc" \
      org.label-schema.version=$GITVERSION
