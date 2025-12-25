#!/bin/bash

# Post-start script for IntelliJ IDEA DevContainer
echo "🔄 Starting IntelliJ IDEA development environment..."

# Source SDKMAN
source ~/.sdkman/bin/sdkman-init.sh

# Check Java installation
java -version
mvn -version
gradle -version

# Start IntelliJ IDEA in background if DISPLAY is set
if [ ! -z "$DISPLAY" ]; then
    echo "🖥️ Starting IntelliJ IDEA GUI..."
    /opt/intellij-idea-ultimate/bin/idea.sh &
fi

echo "✨ Development environment is ready!"