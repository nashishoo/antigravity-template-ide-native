# 🪐 Antigravity Workspace (IDE-Native Edition)

**Kit de inicio para desarrollo paralelo con Agentes de IA en Antigravity IDE.**

![Architecture](https://img.shields.io/badge/Architecture-Parallel_Workers-purple)
![Workflow](https://img.shields.io/badge/Workflow-Head_Architect-blue)

## 🌟 Filosofía: "El Arquitecto y sus Trabajadores"

Este template ha sido optimizado para trabajar **exclusivamente dentro del IDE Antigravity**, eliminando la necesidad de scripts de Python externos o claves de API complejas.

El flujo de trabajo es **100% Paralelo y Delegativo**:

1.  **Tú + Ventana Principal** = **Head Architect**.
2.  **Otras Ventanas** = **Specialist Workers (Coder, Reviewer, etc.)**.

## 🚀 Cómo Empezar (Day 1)

No tienes que instalar nada. Tu IDE ya tiene todo lo necesario.

### 1. Define tu Misión
Edita el archivo `mission.md` con el objetivo de tu proyecto.
> Ej: "Crear una API REST para gestión de inventario."

### 2. Activa al Arquitecto
En la ventana principal de chat, di:
> "He actualizado la misión. Actúa como Arquitecto y dame los prompts para mis workers."

### 3. Distribuye el Trabajo (Parallel Mode)
El Arquitecto analizará tu misión, **buscará skills útiles** y te dará bloques de texto listos para copiar y pegar.
*   **Abre una nueva ventana de chat** -> Pega el prompt del **Coder**.
*   **Abre otra ventana** -> Pega el prompt del **Reviewer**.

¡Tus agentes trabajarán en paralelo con superpoderes instalados!

## ✨ Características Nativas

### 🧠 Memoria Persistente (`planning-with-files`)
El template incluye una skill nativa para gestionar memoria a largo plazo.
*   Tus agentes crearán automáticamente `task_plan.md` y `findings.md`.
*   Esto les permite recordar decisiones complejas entre sesiones.

### 🕵️ Skill Scouting
El Arquitecto tiene la capacidad de buscar nuevas herramientas en `skills.sh` y sugerirte su instalación automática en los prompts de trabajo.

## 📂 Estructura del Proyecto

```
.agent/workflows/   # Definiciones de roles y flujos (Architect, Swarm)
.context/           # Reglas automáticas (Coding Style)
src/tools/          # Herramientas personalizadas (Python)
src/skills/         # Skills instaladas (planning-with-files, etc.)
openspec/           # Sistema de gestión de cambios (Specs)
mission.md          # Objetivo del proyecto
artifacts/          # Planes y documentación generada
```

## 🛠️ Herramientas
Cualquier script Python que pongas en `src/tools/` será automáticamente detectado por los agentes. ¡Úsalo para crear utilidades específicas para tu proyecto!

## 🤝 OpenSpec
Para cambios complejos, usa el sistema OpenSpec en la carpeta `openspec/`.

## 🙏 Créditos y Licencia
Este proyecto es un **Fork IDE-Nativo** del [Antigravity Workspace Template](https://github.com/filosofia-codigo/antigravity-workspace-template) original.
*   **Licencia**: MIT (Ver `LICENSE`).
*   **Autor Original**: Jingwen Fan.
*   **Edición IDE-Nativa (2026)**: Desarrollada por **Catapaz** en colaboración con **Gemini 3**.
*   **Modificaciones**: Adaptado para ejecución paralela sin dependencias de Python/API externas.
