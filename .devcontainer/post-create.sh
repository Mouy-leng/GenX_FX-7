#!/bin/bash

# Post-create script for IntelliJ IDEA DevContainer
echo "🚀 Setting up IntelliJ IDEA development environment..."

# Source SDKMAN
source ~/.sdkman/bin/sdkman-init.sh

# Set Java 17 as default
sdk default java 17.0.9-tem

# Create IntelliJ configuration directories
mkdir -p ~/.config/JetBrains/IntelliJIdea2023.3/{config,system,plugins,logs}

# Create workspace directories
mkdir -p ~/workspace/{java,kotlin,spring,maven,gradle}

# Create common project templates
cd ~/workspace/java
cat > HelloWorld.java << 'EOF'
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World from IntelliJ DevContainer!");
    }
}
EOF

cd ~/workspace/maven
cat > pom.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.a69v.example</groupId>
    <artifactId>maven-template</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
        </plugins>
    </build>
</project>
EOF

mkdir -p src/main/java/com/a69v/example src/test/java/com/a69v/example

cd ~/workspace/gradle
cat > build.gradle << 'EOF'
plugins {
    id 'java'
    id 'application'
}

group = 'com.a69v.example'
version = '1.0.0'
sourceCompatibility = JavaVersion.VERSION_17

repositories {
    mavenCentral()
}

dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
}

application {
    mainClass = 'com.a69v.example.App'
}

test {
    useJUnitPlatform()
}
EOF

mkdir -p src/main/java/com/a69v/example src/test/java/com/a69v/example

# Create IntelliJ settings
cd ~/.config/JetBrains/IntelliJIdea2023.3/config
mkdir -p options codestyles keymaps

# Create optimized IDE settings
cat > options/ide.general.xml << 'EOF'
<application>
  <component name="GeneralSettings">
    <option name="confirmExit" value="false" />
    <option name="showTipsOnStartup" value="false" />
    <option name="reopenLastProject" value="true" />
    <option name="autoSaveFiles" value="true" />
    <option name="synchronizeOnFrameActivation" value="true" />
  </component>
</application>
EOF

# Set up version control
git config --global user.name "A6-9V Developer"
git config --global user.email "developer@a6-9v.local"
git config --global init.defaultBranch main

echo "✅ IntelliJ IDEA development environment setup complete!"
echo "📁 Workspace created at ~/workspace/"
echo "🔧 Java versions available: $(sdk list java | grep installed)"
echo "🎯 Use 'idea.sh' to launch IntelliJ IDEA"