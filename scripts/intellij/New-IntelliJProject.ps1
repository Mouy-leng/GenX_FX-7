# New-IntelliJProject.ps1 - Create new IntelliJ IDEA projects with templates
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$ProjectName,
    
    [Parameter()]
    [ValidateSet("Java", "Maven", "Gradle", "Spring", "Kotlin")]
    [string]$ProjectType = "Java",
    
    [Parameter()]
    [string]$GroupId = "com.a69v",
    
    [Parameter()]
    [string]$ArtifactId,
    
    [Parameter()]
    [string]$Version = "1.0.0",
    
    [Parameter()]
    [string]$JavaVersion = "17",
    
    [Parameter()]
    [string]$OutputPath = ".\Projects",
    
    [Parameter()]
    [switch]$OpenInIntelliJ
)

$ErrorActionPreference = "Stop"

function Write-ProjectBanner {
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║                 📦 IntelliJ Project Creator                  ║
║                        A6-9V Edition                         ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Blue
}

function New-JavaProject {
    param($ProjectPath, $ProjectName)
    
    Write-Host "☕ Creating Java project: $ProjectName" -ForegroundColor Green
    
    # Create directory structure
    $srcDir = New-Item -ItemType Directory -Path "$ProjectPath\src\main\java\com\a69v\$($ProjectName.ToLower())" -Force
    $testDir = New-Item -ItemType Directory -Path "$ProjectPath\src\test\java\com\a69v\$($ProjectName.ToLower())" -Force
    $resourcesDir = New-Item -ItemType Directory -Path "$ProjectPath\src\main\resources" -Force
    
    # Create main class
    $mainClass = @"
package com.a69v.$($ProjectName.ToLower());

/**
 * Main class for $ProjectName
 * Created by A6-9V
 */
public class ${ProjectName}Application {
    public static void main(String[] args) {
        System.out.println("Hello from $ProjectName!");
        System.out.println("🚀 A6-9V Java Application Started");
    }
}
"@
    
    Set-Content -Path "$srcDir\${ProjectName}Application.java" -Value $mainClass
    
    # Create test class
    $testClass = @"
package com.a69v.$($ProjectName.ToLower());

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Test class for ${ProjectName}Application
 */
class ${ProjectName}ApplicationTest {
    
    @Test
    void testApplicationRuns() {
        // Test that the application can be instantiated
        ${ProjectName}Application app = new ${ProjectName}Application();
        assertNotNull(app);
    }
    
    @Test
    void testMainMethod() {
        // Test that main method doesn't throw exceptions
        assertDoesNotThrow(() -> {
            ${ProjectName}Application.main(new String[]{});
        });
    }
}
"@
    
    Set-Content -Path "$testDir\${ProjectName}ApplicationTest.java" -Value $testClass
}

function New-MavenProject {
    param($ProjectPath, $ProjectName, $GroupId, $ArtifactId, $Version, $JavaVersion)
    
    Write-Host "🔨 Creating Maven project: $ProjectName" -ForegroundColor Green
    
    if (-not $ArtifactId) { $ArtifactId = $ProjectName.ToLower() }
    
    # Create Maven structure
    New-JavaProject -ProjectPath $ProjectPath -ProjectName $ProjectName
    
    # Create pom.xml
    $pomXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>$GroupId</groupId>
    <artifactId>$ArtifactId</artifactId>
    <version>$Version</version>
    <packaging>jar</packaging>
    
    <name>$ProjectName</name>
    <description>$ProjectName - A6-9V Project</description>
    
    <properties>
        <maven.compiler.source>$JavaVersion</maven.compiler.source>
        <maven.compiler.target>$JavaVersion</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <junit.version>5.10.0</junit.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>`${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>$JavaVersion</source>
                    <target>$JavaVersion</target>
                </configuration>
            </plugin>
            
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
            
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>3.1.0</version>
                <configuration>
                    <mainClass>com.a69v.$($ProjectName.ToLower()).${ProjectName}Application</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"@
    
    Set-Content -Path "$ProjectPath\pom.xml" -Value $pomXml
}

function New-GradleProject {
    param($ProjectPath, $ProjectName, $GroupId, $ArtifactId, $Version, $JavaVersion)
    
    Write-Host "🐘 Creating Gradle project: $ProjectName" -ForegroundColor Green
    
    if (-not $ArtifactId) { $ArtifactId = $ProjectName.ToLower() }
    
    # Create Gradle structure
    New-JavaProject -ProjectPath $ProjectPath -ProjectName $ProjectName
    
    # Create build.gradle
    $buildGradle = @"
plugins {
    id 'java'
    id 'application'
}

group = '$GroupId'
version = '$Version'
sourceCompatibility = JavaVersion.VERSION_$JavaVersion

repositories {
    mavenCentral()
}

dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

application {
    mainClass = 'com.a69v.$($ProjectName.ToLower()).${ProjectName}Application'
}

test {
    useJUnitPlatform()
}

task runApp(type: JavaExec) {
    classpath = sourceSets.main.runtimeClasspath
    mainClass = 'com.a69v.$($ProjectName.ToLower()).${ProjectName}Application'
}
"@
    
    Set-Content -Path "$ProjectPath\build.gradle" -Value $buildGradle
    
    # Create gradle.properties
    $gradleProperties = @"
# A6-9V Gradle Properties
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configureondemand=true
"@
    
    Set-Content -Path "$ProjectPath\gradle.properties" -Value $gradleProperties
    
    # Create settings.gradle
    $settingsGradle = "rootProject.name = '$ArtifactId'"
    Set-Content -Path "$ProjectPath\settings.gradle" -Value $settingsGradle
}

function New-SpringProject {
    param($ProjectPath, $ProjectName, $GroupId, $ArtifactId, $Version, $JavaVersion)
    
    Write-Host "🍃 Creating Spring Boot project: $ProjectName" -ForegroundColor Green
    
    # Create Maven Spring Boot project
    New-MavenProject -ProjectPath $ProjectPath -ProjectName $ProjectName -GroupId $GroupId -ArtifactId $ArtifactId -Version $Version -JavaVersion $JavaVersion
    
    # Override pom.xml with Spring Boot dependencies
    $springPomXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.5</version>
        <relativePath/>
    </parent>
    
    <groupId>$GroupId</groupId>
    <artifactId>$ArtifactId</artifactId>
    <version>$Version</version>
    <packaging>jar</packaging>
    
    <name>$ProjectName</name>
    <description>$ProjectName - A6-9V Spring Boot Application</description>
    
    <properties>
        <java.version>$JavaVersion</java.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"@
    
    Set-Content -Path "$ProjectPath\pom.xml" -Value $springPomXml
    
    # Create Spring Boot main class
    $springMainClass = @"
package com.a69v.$($ProjectName.ToLower());

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Spring Boot Application for $ProjectName
 * Created by A6-9V
 */
@SpringBootApplication
@RestController
public class ${ProjectName}Application {
    
    public static void main(String[] args) {
        System.out.println("🚀 Starting $ProjectName - A6-9V Spring Boot Application");
        SpringApplication.run(${ProjectName}Application.class, args);
    }
    
    @GetMapping("/")
    public String home() {
        return "Hello from $ProjectName! 🚀 A6-9V Spring Boot Application";
    }
    
    @GetMapping("/health")
    public String health() {
        return "✅ $ProjectName is running!";
    }
}
"@
    
    $srcDir = "src\main\java\com\a69v\$($ProjectName.ToLower())"
    Set-Content -Path "$ProjectPath\$srcDir\${ProjectName}Application.java" -Value $springMainClass
}

function New-README {
    param($ProjectPath, $ProjectName, $ProjectType)
    
    $readme = @"
# $ProjectName

A6-9V $ProjectType Project

## Description
$ProjectName is a $ProjectType project created with the A6-9V IntelliJ project template.

## Getting Started

### Prerequisites
- Java $JavaVersion or higher
- IntelliJ IDEA

### Building and Running

#### For Maven projects:
``````bash
mvn clean compile
mvn exec:java
``````

#### For Gradle projects:
``````bash
./gradlew build
./gradlew run
``````

#### For Spring Boot projects:
``````bash
mvn spring-boot:run
``````

## Project Structure
``````
$ProjectName/
├── src/
│   ├── main/
│   │   ├── java/
│   │   └── resources/
│   └── test/
│       └── java/
├── pom.xml (Maven) or build.gradle (Gradle)
└── README.md
``````

## Development

This project was created using the A6-9V IntelliJ project template system.

### Running Tests
- Maven: `mvn test`
- Gradle: `./gradlew test`

## License
Private A6-9V Project

---
Created by A6-9V Development Tools
"@
    
    Set-Content -Path "$ProjectPath\README.md" -Value $readme
}

function New-GitIgnore {
    param($ProjectPath)
    
    $gitignore = @"
# Compiled class file
*.class

# Log file
*.log

# BlueJ files
*.ctxt

# Mobile Tools for Java (J2ME)
.mtj.tmp/

# Package Files
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# Virtual machine crash logs
hs_err_pid*

# IDE files
.idea/
*.iml
*.ipr
*.iws
.vscode/

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# Gradle
.gradle/
build/
gradle-app.setting
!gradle-wrapper.jar
!gradle-wrapper.properties

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# A6-9V specific
.a69v/
temp/
"@
    
    Set-Content -Path "$ProjectPath\.gitignore" -Value $gitignore
}

# Main execution
try {
    Write-ProjectBanner
    
    if (-not $ArtifactId) { $ArtifactId = $ProjectName.ToLower() }
    
    # Create project directory
    $projectPath = Join-Path $OutputPath $ProjectName
    if (Test-Path $projectPath) {
        Write-Warning "⚠️ Project directory already exists: $projectPath"
        $response = Read-Host "Do you want to continue? (y/N)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Host "❌ Project creation cancelled." -ForegroundColor Red
            exit 0
        }
    }
    
    $null = New-Item -ItemType Directory -Path $projectPath -Force
    
    # Create project based on type
    switch ($ProjectType) {
        "Java" { New-JavaProject -ProjectPath $projectPath -ProjectName $ProjectName }
        "Maven" { New-MavenProject -ProjectPath $projectPath -ProjectName $ProjectName -GroupId $GroupId -ArtifactId $ArtifactId -Version $Version -JavaVersion $JavaVersion }
        "Gradle" { New-GradleProject -ProjectPath $projectPath -ProjectName $ProjectName -GroupId $GroupId -ArtifactId $ArtifactId -Version $Version -JavaVersion $JavaVersion }
        "Spring" { New-SpringProject -ProjectPath $projectPath -ProjectName $ProjectName -GroupId $GroupId -ArtifactId $ArtifactId -Version $Version -JavaVersion $JavaVersion }
        "Kotlin" { 
            Write-Warning "Kotlin template not yet implemented. Creating Java template instead."
            New-JavaProject -ProjectPath $projectPath -ProjectName $ProjectName 
        }
    }
    
    # Create common files
    New-README -ProjectPath $projectPath -ProjectName $ProjectName -ProjectType $ProjectType
    New-GitIgnore -ProjectPath $projectPath
    
    Write-Host "✅ Project '$ProjectName' created successfully!" -ForegroundColor Green
    Write-Host "📁 Location: $projectPath" -ForegroundColor Cyan
    
    # Initialize Git repository
    Push-Location $projectPath
    try {
        git init
        git add .
        git commit -m "Initial commit - A6-9V $ProjectType project: $ProjectName"
        Write-Host "🔧 Git repository initialized" -ForegroundColor Green
    } catch {
        Write-Warning "⚠️ Git initialization failed: $_"
    }
    Pop-Location
    
    # Open in IntelliJ if requested
    if ($OpenInIntelliJ) {
        $startScript = Join-Path $PSScriptRoot "Start-IntelliJ.ps1"
        if (Test-Path $startScript) {
            Write-Host "🚀 Opening project in IntelliJ IDEA..." -ForegroundColor Blue
            & $startScript -ProjectPath $projectPath
        } else {
            Write-Warning "⚠️ Start-IntelliJ.ps1 not found. Please open the project manually."
        }
    }
    
} catch {
    Write-Error "❌ Failed to create project: $_"
    exit 1
}

# Example usage:
# .\New-IntelliJProject.ps1 "MyApp" -ProjectType "Maven" -OpenInIntelliJ
# .\New-IntelliJProject.ps1 "SpringDemo" -ProjectType "Spring" -GroupId "com.a69v" -JavaVersion "17"