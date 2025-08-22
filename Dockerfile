# Start from the fredericklab base container
FROM fredericklab/basecontainer:latest-release

# get build arguments
ARG BUILD_TIME
ARG BRANCH
ARG GITVERSION
ARG GITDIRECTVERSION
ARG GITSHA
ARG GITDATE

# set and echo environment variables
ENV BUILD_TIME=$BUILD_TIME
ENV BRANCH=$BRANCH
ENV GITVERSION=${GITVERSION}
ENV GITSHA=${GITSHA}
ENV GITDATE=${GITDATE}
ENV GITDIRECTVERSION=${GITDIRECTVERSION}

RUN echo "BRANCH: "$BRANCH
RUN echo "BUILD_TIME: "$BUILD_TIME
RUN echo "GITVERSION: "$GITVERSION
RUN echo "GITSHA: "$GITSHA
RUN echo "GITDATE: "$GITDATE
RUN echo "GITDIRECTVERSION: "$GITDIRECTVERSION

# security patches
RUN uv pip install "cryptography>=42.0.4" "urllib3>=1.26.17"

# copy capcalc into container
COPY . /src/capcalc
RUN echo $GITVERSION > /src/capcalc/VERSION

# init and install capcalc
RUN uv pip install --upgrade pip
RUN cd /src/capcalc && \
    uv pip install .
RUN chmod -R a+r /src/capcalc

# clean up build directories
RUN rm -rf /src/picachooser/build /src/picachooser/dist

# update the paths to libraries
RUN ldconfig

# set a flag so we know we're in a container
ENV RUNNING_IN_CONTAINER=1

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
ENV HOME="/home/capcalc"

# initialize user mamba
RUN /opt/miniforge3/bin/mamba shell
RUN echo "mamba activate science" >> /home/capcalc/.bashrc

# set to non-root user
USER capcalc

# set up variable for non-interactive shell
ENV PATH=/opt/miniforge3/envs/science/bin:/opt/miniforge3/condabin:.:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /tmp/

ENTRYPOINT ["/opt/miniforge3/envs/science/bin/capcalc_dispatcher"]

LABEL org.label-schema.build-date=$BUILD_TIME \
      org.label-schema.name="capcalc" \
      org.label-schema.description="capcalc - coactivation pattern analysis software" \
      org.label-schema.url="http://nirs-fmri.net" \
      org.label-schema.vcs-ref=$GITVERSION \
      org.label-schema.vcs-url="https://github.com/bbfrederick/capcalc" \
      org.label-schema.version=$GITVERSION
