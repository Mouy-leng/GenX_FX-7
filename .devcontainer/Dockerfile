ARG VARIANT=17-jdk-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/java:${VARIANT}

# Install IntelliJ IDEA Ultimate
ARG INTELLIJ_VERSION=2023.3.2
ARG INTELLIJ_HOME=/opt/intellij-idea-ultimate

USER root

# Update system and install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    tar \
    git \
    build-essential \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libfreetype6 \
    libfontconfig1 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install IntelliJ IDEA Ultimate
RUN mkdir -p ${INTELLIJ_HOME} && \
    wget -q "https://download.jetbrains.com/idea/ideaIU-${INTELLIJ_VERSION}.tar.gz" -O /tmp/intellij.tar.gz && \
    tar -xzf /tmp/intellij.tar.gz -C ${INTELLIJ_HOME} --strip-components=1 && \
    rm /tmp/intellij.tar.gz && \
    chmod +x ${INTELLIJ_HOME}/bin/idea.sh

# Create IntelliJ desktop entry
RUN echo "[Desktop Entry]\n\
Version=1.0\n\
Type=Application\n\
Name=IntelliJ IDEA Ultimate\n\
Icon=${INTELLIJ_HOME}/bin/idea.svg\n\
Exec=${INTELLIJ_HOME}/bin/idea.sh\n\
Comment=Capable and Ergonomic IDE for JVM\n\
Categories=Development;IDE;\n\
Terminal=false\n\
StartupWMClass=jetbrains-idea" > /usr/share/applications/intellij-idea-ultimate.desktop

# Install additional development tools
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    htop \
    tree \
    jq \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install SDKMAN and additional Java versions
USER vscode
RUN curl -s "https://get.sdkman.io" | bash
RUN bash -c "source ~/.sdkman/bin/sdkman-init.sh && \
    sdk install java 11.0.21-tem && \
    sdk install java 8.0.392-tem && \
    sdk install maven && \
    sdk install gradle && \
    sdk install kotlin"

# Setup IntelliJ configuration directory
RUN mkdir -p /home/vscode/.config/JetBrains/IntelliJIdea2023.3

USER root

# Add IntelliJ to PATH
ENV PATH="${INTELLIJ_HOME}/bin:${PATH}"

# Set display for GUI applications
ENV DISPLAY=:0.0

# Switch back to vscode user
USER vscode

# Create workspace directory
RUN mkdir -p /home/vscode/workspace