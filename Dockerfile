# Start from the fredericklab base container
FROM fredericklab/basecontainer:v0.3.0

# get build arguments
ARG BUILD_TIME
ARG BRANCH
ARG GITVERSION
ARG GITSHA
ARG GITDATE

# set and echo environment variables
ENV BUILD_TIME $BUILD_TIME
ENV BRANCH $BRANCH
ENV GITVERSION=${GITVERSION}
ENV GITSHA=${GITSHA}
ENV GITDATE=${GITDATE}

RUN echo "BRANCH: "$BRANCH
RUN echo "BUILD_TIME: "$BUILD_TIME
RUN echo "GITVERSION: "$GITVERSION
RUN echo "GITSHA: "$GITSHA
RUN echo "GITDATE: "$GITDATE

# Install capcalc
COPY . /src/capcalc
RUN echo $GITVERSION > /src/capcalc/VERSION
RUN cd /src/capcalc && \
    pip install . && \
    rm -rf /src/capcalc/build /src/capcalc/dist

# clean up
#RUN mamba clean -y --all
RUN pip cache purge

# Create a shared $HOME directory
RUN useradd -m -s /bin/bash -G users capcalc
WORKDIR /home/capcalc
ENV HOME="/home/capcalc"

ENV IS_DOCKER_8395080871=1

RUN ldconfig
WORKDIR /tmp/
ENTRYPOINT ["capcalc_dispatcher"]

# set a non-root user
USER capcalc

LABEL org.label-schema.build-date=$BUILD_TIME \
      org.label-schema.name="capcalc" \
      org.label-schema.description="capcalc - a set of tools for delay processing" \
      org.label-schema.url="http://nirs-fmri.net" \
      org.label-schema.vcs-ref=$GITVERSION \
      org.label-schema.vcs-url="https://github.com/bbfrederick/capcalc" \
      org.label-schema.version=$GITVERSION
