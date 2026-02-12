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

No requiere instalación. Tu IDE ya tiene todo lo que necesita.
> **¿Atascado?** Revisa la [Guía de Problemas](docs/TROUBLESHOOTING_ES.md) o la **[Guía Detallada](docs/DETAILED_GUIDE_ES.md)**.

### 1. Configura la Misión (Los Cimientos)
Abre `mission.md`. Este archivo contiene el **System Prompt** que guía al Arquitecto.

> **💡 Pro Tip:** No escribas la misión desde cero. Usa un modelo superior (Sonnet 4.5, GPT-5, Gemini 3 Pro) para generar un Objetivo y Descripción robustos. Mira la **[Guía Detallada](docs/DETAILED_GUIDE_ES.md)** para ver el prompt recomendado.

*   **Edita**: Reemplaza el "Objective" por defecto con tu meta real.
*   **Guarda**: Asegúrate de guardar. los cambios.

### 2. Activa al Arquitecto
1.  **Selecciona Todo**: Copia el *contenido completo* de `mission.md` (Ctrl+A, Ctrl+C).
2.  **Pega**: Ve a la **Ventana Principal de Chat** y pega el contenido.
3.  **Envía**: El Arquitecto analizará tu misión y generará los siguientes pasos.

### 3. Distribuye el Trabajo (Modo Paralelo)
El Arquitecto te devolverá **Prompts para Trabajadores** (tareas formateadas para roles específicos).
1.  **Abre Nuevas Ventanas**: Abre tantas ventanas de Antigravity como necesites (ej: una para Coder, otra para Reviewer).
2.  **Pega y Ejecuta**: Copia el prompt específico para cada rol en su propia ventana.
3.  **Monitorea**: Tus agentes ahora están trabajando en paralelo, con contexto completo.

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
skills_registry.json # Registro local de skills
src/tools/          # Herramientas personalizadas (Python, opcional)
src/skills/         # Skills instaladas (planning-with-files, etc.)
.agent/skills/      # Paquetes de skills (opcional)
.agents/skills/     # Paquetes de skills (opcional)
.github/skills/     # Skills compartidas (opcional)
.claude/skills/     # Skills compatibles con Claude (opcional)
.codex/skills/      # Skills compatibles con Codex (opcional)
.cursor/skills/     # Skills compatibles con Cursor (opcional)
.vscode/skills/     # Skills compatibles con VS Code (opcional)
openspec/           # Sistema de gestion de cambios (Specs)
mission.md          # Objetivo del proyecto
artifacts/          # Planes y documentacion generada
```

## Herramientas
Cualquier script Python que agregues a `src/tools/` sera detectado automaticamente por los agentes. Usa esta carpeta para utilidades especificas del proyecto.
*   **`src/tools/skills_catalog.py`**: Lista skills locales en todos los roots soportados y consulta el registro local.

## OpenSpec
Para cambios complejos, usa el sistema OpenSpec en la carpeta `openspec/`.

## Creditos y Licencia
Este proyecto es un **Fork IDE-Nativo** del [Antigravity Workspace Template](https://github.com/filosofia-codigo/antigravity-workspace-template) original.
* **Licencia**: MIT (ver `LICENSE`).
* **Autor Original**: Jingwen Fan.
* **Edicion IDE-Nativa (2026)**: Desarrollada por **Catapaz** en colaboracion con **Gemini 3**.
* **Modificaciones**: Adaptado para ejecucion paralela sin dependencias de Python/API externas.





