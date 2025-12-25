# IntelliJ IDEA Optimization Suite - A6-9V Edition

Complete automation and optimization setup for IntelliJ IDEA development, similar to the PyCharm setup but tailored for Java/JVM development.

## 🚀 Features

### DevContainer Support
- **Full IntelliJ IDEA Ultimate** in containerized environment
- **Multi-language support**: Java 8/11/17, Kotlin, Node.js, Python
- **Build tools**: Maven, Gradle, SDKMAN integration
- **Development tools**: Git, Docker-in-Docker, debugging support

### Automation Scripts
- **IntelliJ-Manager.ps1**: Master control script for all operations
- **Start-IntelliJ.ps1**: Optimized launcher with memory management
- **New-IntelliJProject.ps1**: Project template generator
- **Optimize-IntelliJ.ps1**: Performance tuning and maintenance

### Project Templates
- **Java**: Basic Java project with JUnit 5
- **Maven**: Standard Maven project with A6-9V conventions
- **Gradle**: Gradle project with optimization settings
- **Spring Boot**: Complete Spring Boot web application
- **Kotlin**: (Planned) Kotlin project template

## 📁 File Structure

```
Desktop/
├── .devcontainer/
│   ├── devcontainer.json       # VS Code DevContainer configuration
│   ├── Dockerfile             # IntelliJ IDEA container setup
│   ├── post-create.sh         # Container initialization script
│   └── post-start.sh          # Container startup script
├── scripts/intellij/
│   ├── IntelliJ-Manager.ps1   # Master automation script
│   ├── Start-IntelliJ.ps1     # IntelliJ launcher with optimizations
│   ├── New-IntelliJProject.ps1 # Project template creator
│   └── Optimize-IntelliJ.ps1  # Performance optimization tool
├── templates/intellij/
│   └── ide-settings.xml       # Optimized IntelliJ settings
└── IntelliJ-Optimization-README.md
```

## 🛠️ Quick Start

### 1. Master Command Interface
```powershell
# Show help and available commands
.\scripts\intellij\IntelliJ-Manager.ps1

# Start IntelliJ IDEA with optimizations
.\scripts\intellij\IntelliJ-Manager.ps1 Start

# Create new Maven project
.\scripts\intellij\IntelliJ-Manager.ps1 New "MyApp" -ProjectType Maven

# Optimize IntelliJ performance
.\scripts\intellij\IntelliJ-Manager.ps1 Optimize

# Check system status
.\scripts\intellij\IntelliJ-Manager.ps1 Status
```

### 2. Individual Script Usage
```powershell
# Start IntelliJ with specific project
.\scripts\intellij\Start-IntelliJ.ps1 -ProjectPath "C:\Projects\MyApp" -MaxMemory 8192

# Create Spring Boot project
.\scripts\intellij\New-IntelliJProject.ps1 "SpringDemo" -ProjectType Spring -GroupId "com.a69v"

# Full optimization with cache clearing
.\scripts\intellij\Optimize-IntelliJ.ps1 -All -Fresh
```

## 🐳 DevContainer Setup

### Prerequisites
- Docker Desktop for Windows
- VS Code with Dev Containers extension

### Usage
1. Open project in VS Code
2. Command Palette → "Dev Containers: Reopen in Container"
3. Container will build with IntelliJ IDEA Ultimate pre-installed
4. Access IntelliJ via X11 forwarding or web interface

### Container Features
- **IntelliJ IDEA Ultimate 2023.3.2**
- **Java versions**: 8, 11, 17 (via SDKMAN)
- **Build tools**: Maven, Gradle, latest versions
- **Additional tools**: Git, Docker, development utilities
- **Optimized performance**: Pre-configured memory settings

## ⚙️ Optimization Features

### Memory Management
- **Automatic memory allocation** based on system RAM
- **Optimized garbage collection** settings (G1GC)
- **JVM tuning** for IntelliJ performance
- **Cache management** with selective clearing

### Performance Settings
- **Disabled animations** and visual effects
- **Optimized indexing** settings
- **Limited tab count** and history
- **Efficient file watching** configuration

### Development Environment
- **A6-9V conventions**: Project templates with organization standards
- **Git integration**: Pre-configured with A6-9V user settings
- **Code style**: 120-character line limit, consistent formatting
- **Plugin recommendations**: Essential plugins for Java development

## 📦 Project Templates

### Maven Project Structure
```
MyApp/
├── src/main/java/com/a69v/myapp/
│   └── MyAppApplication.java
├── src/test/java/com/a69v/myapp/
│   └── MyAppApplicationTest.java
├── src/main/resources/
├── pom.xml
├── README.md
└── .gitignore
```

### Spring Boot Features
- **Web starter** dependency
- **Testing framework** (JUnit 5, Spring Boot Test)
- **Health endpoint** at `/health`
- **Maven exec plugin** configuration
- **A6-9V branding** in application output

## 🔧 Maintenance Commands

### Cache Management
```powershell
# Clear all IntelliJ caches
.\scripts\intellij\Optimize-IntelliJ.ps1 -ClearCache

# Backup settings before optimization
.\scripts\intellij\Optimize-IntelliJ.ps1 -BackupSettings

# Restore previous settings
.\scripts\intellij\Optimize-IntelliJ.ps1 -RestoreSettings
```

### Memory Optimization
```powershell
# Optimize for current system
.\scripts\intellij\Optimize-IntelliJ.ps1 -OptimizeMemory

# Check current status
.\scripts\intellij\Optimize-IntelliJ.ps1 | Select-String "Memory"
```

## 🎯 Recommended Plugins

The optimization suite recommends these essential plugins:

- **Maven Helper**: Enhanced Maven support
- **Gradle**: Advanced Gradle integration  
- **Spring Boot**: Spring framework support
- **Lombok**: Annotation processing
- **GitToolBox**: Enhanced Git integration
- **SonarLint**: Code quality analysis
- **CheckStyle-IDEA**: Code style enforcement
- **Docker**: Container development support
- **Rainbow Brackets**: Code readability
- **Key Promoter X**: Shortcut learning

## 🚀 Advanced Usage

### Custom Project Types
```powershell
# Create with custom settings
.\scripts\intellij\New-IntelliJProject.ps1 "MyApp" -ProjectType Maven `
    -GroupId "com.a69v.custom" -JavaVersion "11" -OutputPath "D:\Projects"
```

### Performance Tuning
```powershell
# Maximum performance mode
.\scripts\intellij\Start-IntelliJ.ps1 -MaxMemory 16384 -Fresh
```

### DevContainer Customization
Edit `.devcontainer/devcontainer.json` to:
- Change Java versions
- Add custom tools
- Modify port forwarding
- Configure VS Code extensions

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free space
- **Java**: JDK 11+ (handled by scripts)

### Optimal Configuration  
- **RAM**: 16GB+ (allows 8GB+ heap for IntelliJ)
- **CPU**: Multi-core processor
- **Storage**: SSD recommended
- **Docker**: For DevContainer support

## 🔗 Integration with A6-9V Workflow

### Git Configuration
- User name: "A6-9V Developer"
- Email: "developer@a6-9v.local"  
- Default branch: "main"

### Project Conventions
- Group ID: "com.a69v"
- Package naming: `com.a69v.projectname`
- Code style: 120-character line limit
- Documentation: README with A6-9V template

### Build Integration
- Maven: Optimized settings in templates
- Gradle: Performance-tuned gradle.properties
- Testing: JUnit 5 with comprehensive test templates

## 🆘 Troubleshooting

### Common Issues
1. **IntelliJ not found**: Check installation paths in Start-IntelliJ.ps1
2. **Memory issues**: Reduce MaxMemory parameter or increase system RAM
3. **DevContainer fails**: Ensure Docker Desktop is running
4. **Java not found**: Scripts will help install Java via SDKMAN

### Debug Mode
```powershell
# Enable detailed logging
.\scripts\intellij\IntelliJ-Manager.ps1 Start -Debug
```

### Support
- Check system status: `.\scripts\intellij\IntelliJ-Manager.ps1 Status`
- Review logs in IntelliJ IDEA installation directory
- Use backup/restore features for settings recovery

---

## 🎉 Next Steps

1. Run `.\scripts\intellij\IntelliJ-Manager.ps1 Status` to verify setup
2. Create your first project with `IntelliJ-Manager.ps1 New "TestApp"`
3. Optimize performance with `IntelliJ-Manager.ps1 Optimize`
4. Explore DevContainer development environment

**Happy coding with A6-9V IntelliJ IDEA optimization! 🚀**