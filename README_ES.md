# Antigravity Workspace (IDE-Native Edition)

**Kit de inicio para desarrollo paralelo con agentes de IA dentro de Antigravity IDE.**

![Architecture](https://img.shields.io/badge/Architecture-Parallel_Workers-purple)
![Workflow](https://img.shields.io/badge/Workflow-Head_Architect-blue)

## Filosofia: "El Arquitecto y sus Trabajadores"

Este template esta optimizado para funcionar **completamente dentro del IDE Antigravity**, eliminando la necesidad de motores Python externos o configuraciones de API complejas.

El flujo de trabajo es **100% paralelo y delegativo**:

1. **Tu + Ventana Principal** = **Head Architect**.
2. **Otras Ventanas** = **Specialist Workers (Coder, Reviewer, etc.)**.

## Como Empezar (Day 1)

No necesitas instalar nada. Tu IDE ya tiene todo lo necesario.
> **¿Atascado?** Revisa la [Guía de Solución de Problemas](docs/TROUBLESHOOTING_ES.md).

### 1. Define tu Mision
Edita `mission.md` con el objetivo de tu proyecto.
> Ejemplo: "Crear una API REST para gestion de inventario."

### 2. Activa al Arquitecto
En la ventana principal de chat, di:
> "He actualizado la mision. Actua como Arquitecto y dame los prompts para mis workers."

### 3. Distribuye el Trabajo (Parallel Mode)
El Arquitecto analizara tu mision, **revisara las skills instaladas**, y te dara prompts listos para copiar y pegar.
* **Abre una nueva ventana de chat** -> Pega el prompt del **Coder**.
* **Abre otra ventana** -> Pega el prompt del **Reviewer**.

Tus agentes trabajaran en paralelo con tooling nativo.

## Caracteristicas Nativas

### Memoria Persistente (`planning-with-files`)
El template incluye una skill nativa para gestionar memoria a largo plazo.
* Tus agentes crean automaticamente `task_plan.md` y `findings.md`.
* Esto permite recordar decisiones complejas entre sesiones.

### Preflight del Arquitecto
Antes de delegar cualquier trabajo, el **Arquitecto** debe ejecutar el flujo de trabajo de preflight para verificar las skills y herramientas disponibles:
*   **Workflow**: `.agent/workflows/preflight.md`
*   **Propósito**: Inventariar skills locales, verificar la CLI de `skills.sh`, y validar la disponibilidad de herramientas.

## Estructura del Proyecto

```
.agent/workflows/   # Definiciones de roles y flujos (Architect, Swarm, Preflight)
.context/           # Reglas automaticas (Coding Style)
src/tools/          # Herramientas personalizadas (Python, opcional)
src/skills/         # Skills instaladas (planning-with-files, etc.)
openspec/           # Sistema de gestion de cambios (Specs)
mission.md          # Objetivo del proyecto
artifacts/          # Planes y documentacion generada
```

## Herramientas
Cualquier script Python que agregues a `src/tools/` sera detectado automaticamente por los agentes. Usa esta carpeta para utilidades especificas del proyecto.
*   **`src/tools/skills_catalog.py`**: Una utilidad para buscar skills en skills.sh y listar skills locales.

## OpenSpec
Para cambios complejos, usa el sistema OpenSpec en la carpeta `openspec/`.

## Creditos y Licencia
Este proyecto es un **Fork IDE-Nativo** del [Antigravity Workspace Template](https://github.com/filosofia-codigo/antigravity-workspace-template) original.
* **Licencia**: MIT (ver `LICENSE`).
* **Autor Original**: Jingwen Fan.
* **Edicion IDE-Nativa (2026)**: Desarrollada por **Catapaz** en colaboracion con **Gemini 3**.
* **Modificaciones**: Adaptado para ejecucion paralela sin dependencias de Python/API externas.
