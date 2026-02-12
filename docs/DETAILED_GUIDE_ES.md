# Antigravity Workspace: Guía Detallada

**Una guía completa sobre el Flujo de Trabajo del Arquitecto Paralelo y características nativas del IDE.**

## 1. Resumen
**Misión:** Proporcionar un entorno de ejecución paralela "cero configuración" para agentes de IA dentro del IDE Antigravity.
**Filosofía Central:** "El Arquitecto y los Trabajadores" - Un modelo de procesamiento paralelo con supervisión humana.

---

## 2. Paso 0: Configuración del Contexto (Los Cimientos)
Antes de que el Arquitecto pueda comenzar, el "Cerebro" de la operación debe configurarse en `mission.md`. Este archivo contiene el Prompt del Sistema que define el objetivo actual del Arquitecto.

### Cómo configurar `mission.md`
El archivo tiene dos partes distintas:
1.  **Núcleo Editable (Líneas 1-6):** Aquí defines QUÉ quieres construir.
2.  **Marco Estático (Líneas 7+):** Define CÓMO trabaja el agente (la persona del Arquitecto Paralelo). **No toques esta parte** a menos que quieras cambiar el comportamiento fundamental del agente.

### Flujo Recomendado: "Prompt Engineering con Modelos Superiores"
No escribas la misión desde cero. Usa un modelo de razonamiento superior (como Sonnet 4.5, Opus 4.6, GPT-5, o Gemini 3 Pro) para generar una declaración de misión de alta calidad.

**Prompt para el Modelo Externo:**
> "Necesito configurar un agente Arquitecto de IA para construir [TU IDEA DE PROYECTO]. Por favor genera un 'Objetivo' y una 'Descripción' concisos pero detallados para un archivo `mission.md`. El objetivo debe ser específico, medible y desglosado en fases de alto nivel. Genera SOLO el texto de Objetivo y Descripción."

**Qué pegar en `mission.md`:**
```markdown
# Agent Mission: Parallel Execution Architect

# [EDIT THIS PART]
**Objective:** [Pega aquí el objetivo generado]

## Description
[Pega aquí la descripción generada]
# [END EDIT]

# [DO NOT TOUCH]
Your primary role is NOT to write all the code yourself...
(Mantén el resto del archivo como está)
```

---

## 3. El Rol del Arquitecto
El agente de la "Ventana Principal" actúa como el **Arquitecto Jefe**.

### Responsabilidades Clave:
1.  **Estrategia y Planificación:** Desglosar misiones de alto nivel en tareas paralelas independientes.
2.  **Exploración de Skills (Preflight):**
    -   El Arquitecto **DEBE** ejecutar el flujo `.agent/workflows/preflight.md` antes de delegar.
    -   **Fuentes de Descubrimiento:**
        1.  **Núcleo Local:** `src/skills/` (ej. `research`, `planning-with-files`).
        2.  **Registro Local:** Rutas personalizadas definidas en `.agent/skills.json`.
        3.  **Remoto:** Catálogo `skills.sh` y repositorio `awesome-agent-skills`.
3.  **Generación de Prompts:**
    -   Crea prompts especializados para "Trabajadores" (Coders, Reviewers, etc.).
    -   **Inyección de Contexto:** Cada prompt incluye un bloque `## CONTEXT` con reglas del proyecto y `## SUGGESTED SKILLS`.

---

## 4. Capacidades de los Workers
Los Workers son agentes especializados que corren en ventanas separadas del IDE. Reciben un prompt de alto contexto del Arquitecto y ejecutan localmente.

### Capacidades:
-   **Ejecución Autónoma:** Tienen acceso completo al sistema de archivos y terminal.
-   **Memoria Persistente:** Confían en la skill **Planning with Files**.
    -   **Mecanismo:** En lugar de mantener todo en contexto, mantienen `task_plan.md`, `findings.md`, y `progress.md` en disco.
    -   **Beneficio:** Permite tareas complejas y largas sin agotar la ventana de contexto.

---

## 5. Arquitectura del Sistema de Skills
El proyecto usa un sistema híbrido (Nativo + Externo).

### Carga de Skills
-   **Descubrimiento Dinámico:** Escanea recursivamente `src/skills/` y cualquier ruta en `.agent/skills.json` al inicio.
-   **Carga Híbrida:**
    -   **Código:** Si existe `tools.py`, sus funciones se registran como herramientas ejecutables.
    -   **Conocimiento:** Si existe `SKILL.md`, su contenido se inyecta en el prompt del sistema.

### Descubrimiento Nativo en IDE
Tu espacio de trabajo está equipado con una capacidad expandida de "Skill Scout":
-   **Flexibilidad Local:** Trae tus propias librerías de skills privadas vía `.agent/skills.json`.
-   **Acceso Comunitario:** El Arquitecto busca herramientas de la comunidad en `awesome-agent-skills`.

---

## 6. Gobernanza
-   **Ejecución Paralela:** Verificada vía `parallel_architect.md`.
    - Flujo: `Usuario -> Arquitecto -> [Contexto + Prompt] -> Worker(s) -> [Código + Artefactos] -> Usuario`.
-   **Gestión de Cambios:** El directorio `openspec/` contiene el modelo de gobernanza para proponer cambios complejos.
