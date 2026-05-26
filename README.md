# Port-Scanner-DIY-V1.0

Este proyecto fue construido con fines educativos y forma parte de mi proceso de formación y armado de portfolio en ciberseguridad.
---

## Objetivo del proyecto

El objetivo principal de este desarrollo fue comprender e implementar manualmente conceptos fundamentales relacionados con:

- Escaneo de puertos TCP
- Concurrencia y multithreading
- Fingerprinting básico de servicios
- Análisis y clasificación de riesgo
- Generación de reportes
- Automatización de tareas de reconocimiento

En lugar de depender inicialmente de herramientas estándar como **Nmap**, el proyecto busca entender la lógica subyacente detrás de este tipo de utilidades mediante una implementación propia en Python.

---

## Características

✔ Escaneo multihilo mediante `ThreadPoolExecutor`  
✔ Modos de escaneo configurables (`Fast`, `Intermediate`, `Full`)  
✔ Modos de comportamiento (`Stealth`, `Audit`, `Aggressive`)  
✔ Banner grabbing y detección básica de versiones  
✔ Motor de clasificación de riesgo por servicio/puerto  
✔ Sistema de recomendaciones (*Hint Engine*)  
✔ Generación de reportes HTML  
✔ Salida legible por consola

---

## Entorno de pruebas

Las validaciones y pruebas del proyecto fueron realizadas dentro de un laboratorio local y controlado de ciberseguridad utilizando:

### Infraestructura

- **Windows Host**
- **VirtualBox**
- **Metasploitable 2** como máquina objetivo vulnerable
- Red **Host-Only** aislada para pruebas seguras

### Target utilizado

**Metasploitable 2** fue utilizado como entorno de validación debido a su exposición intencional de múltiples servicios vulnerables, permitiendo probar distintos escenarios de escaneo y análisis.

Ejemplos de servicios detectados:

- FTP
- SSH
- Telnet
- HTTP
- SMB
- MySQL
- PostgreSQL

---

## Modos disponibles

### Modos de Escaneo

| Modo | Rango |
|------|------|
| Fast | 1–1024 |
| Intermediate | 1–5000 |
| Full | 1–65535 |

### Modos de Comportamiento

| Modo | Características |
|------|------|
| Stealth | Menor cantidad de threads + delays aleatorios |
| Audit | Balance entre velocidad y estabilidad |
| Aggressive | Máxima concurrencia y velocidad |

---
