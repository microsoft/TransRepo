import os
import xml.etree.ElementTree as ET

def create_default_pom(project_path):
    """Create a default pom.xml file"""
    artifact_id = os.path.basename(project_path)
    
    pom_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>{artifact_id}</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>8</source>
                    <target>8</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""
    pom_path = os.path.join(project_path, 'pom.xml')
    try:
        with open(pom_path, 'w', encoding='utf-8') as f:
            f.write(pom_content)
        return True
    except Exception as e:
        print(f"Error creating pom.xml: {str(e)}")
        return False

def setup_jacoco(pom_path):
    """Add JaCoCo plugin to pom.xml"""
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        
        ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}
        
        build = root.find('.//maven:build', ns)
        if build is None:
            build = ET.SubElement(root, 'build')
        
        plugins = build.find('.//maven:plugins', ns)
        if plugins is None:
            plugins = ET.SubElement(build, 'plugins')

        jacoco_exists = False
        for plugin in plugins.findall('.//maven:plugin', ns):
            artifact_id = plugin.find('.//maven:artifactId', ns)
            if artifact_id is not None and artifact_id.text == 'jacoco-maven-plugin':
                jacoco_exists = True
                break

        if not jacoco_exists:
            plugin = ET.SubElement(plugins, 'plugin')
            group_id = ET.SubElement(plugin, 'groupId')
            group_id.text = 'org.jacoco'
            artifact_id = ET.SubElement(plugin, 'artifactId')
            artifact_id.text = 'jacoco-maven-plugin'
            version = ET.SubElement(plugin, 'version')
            version.text = '0.8.8'
            
            executions = ET.SubElement(plugin, 'executions')
            execution1 = ET.SubElement(executions, 'execution')
            goals1 = ET.SubElement(execution1, 'goals')
            goal1 = ET.SubElement(goals1, 'goal')
            goal1.text = 'prepare-agent'
            
            execution2 = ET.SubElement(executions, 'execution')
            id2 = ET.SubElement(execution2, 'id')
            id2.text = 'report'
            phase2 = ET.SubElement(execution2, 'phase')
            phase2.text = 'test'
            goals2 = ET.SubElement(execution2, 'goals')
            goal2 = ET.SubElement(goals2, 'goal')
            goal2.text = 'report'

            tree.write(pom_path, encoding='utf-8', xml_declaration=True)
            return True
    except Exception as e:
        print(f"Error modifying pom.xml: {str(e)}")
        return False
    return True