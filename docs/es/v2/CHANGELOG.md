# Registro de Cambios - v2.0.0-alpha.1

Todos los cambios notables a la **Plantilla de Espacio de Trabajo Antigravity** serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-alpha.1] - 2026-02-14

### Añadido (Fase 1: Sincronización de Contexto)
*   `.context/ACTIVE.md` - **La piedra angular de v2.0.** Un archivo de estado dedicado para rastrear el enfoque actual, líneas de trabajo activas y bloqueos. Resuelve el problema de "Deriva de Contexto" donde los agentes pierden el rastro del estado del proyecto.
*   `specs/active_context_protocol.md` - Especificación formal para el protocolo de Sincronización de Contexto, definiendo el contrato de "Lectura-al-Entrar / Actualización-al-Salir".
*   Directorio `.archive/` - Carpetas estandarizadas para `completed` (completado), `deprecated` (obsoleto) y `snapshots` (instantáneas) para mantener el espacio de trabajo limpio.
*   `src/tools/archive_manager.py` - Herramienta para mover programáticamente archivos al archivo con metadatos (quién lo archivó, cuándo y por qué).
*   `src/tools/plan_sync.py` - Herramienta para analizar `PLAN.md` y sincronizar su estado con `ACTIVE.md`.

### Añadido (Fase 2: Herramientas Python)
*   `src/tools/_common.py` - Utilidades compartidas para resolución de rutas, análisis de ACTIVE.md y registro estandarizado.
*   `src/tools/data_validator.py` - **Capa de Integridad Crítica.** Motor de validación basado en Pydantic que asegura que `ACTIVE.md`, `PLAN.md` y otros archivos de datos se adhieran a sus esquemas.
*   `src/tools/scaffold.py` - Herramienta de automatización para generar nuevas herramientas, archivos de especificaciones y archivos de prueba a partir de plantillas, reduciendo la fatiga del código repetitivo.
*   `src/tools/watchdog_sync.py` - Un demonio que monitorea eventos del sistema de archivos y solicita al usuario/agente actualizar `ACTIVE.md` cuando se modifican archivos.
*   Jerarquía `tests/` - Una suite completa de pytest para todas las nuevas herramientas.
*   `pyproject.toml` - Configuración estandarizada del proyecto Python.

### Cambiado
*   `PLAN.md` - Estructura mejorada para soportar análisis programático. Ahora sirve como la "Memoria a Largo Plazo" mientras que `ACTIVE.md` es la "Memoria a Corto Plazo".
*   `artifacts/` - La estructura ahora se aplica estrictamente (aunque aún no está completamente automatizada hasta la Fase 3).

### Cambios de Arquitectura
*   **Protocolo de Estado Compartido**: Se pasó de "conocimiento implícito" (en la ventana de chat) a "conocimiento explícito" (en `.context/ACTIVE.md`).
*   **Modelo Híbrido (Markdown + Python)**: Ahora distinguimos explícitamente entre *Pensar* (archivos Markdown) y *Hacer* (herramientas Python). v1.0 intentaba hacer todo en Markdown o scripts ad-hoc.
*   **Validación-Primero**: Todos los protocolos centrales ahora tienen herramientas de validación correspondientes. No puedes romper la estructura de `ACTIVE.md` sin que el validador te grite.

### Pruebas
*   Añadidas **49** pruebas unitarias cubriendo todas las herramientas de la Fase 2.
*   Cobertura de pruebas estimada en >90% para `src/tools/`.
*   Ejecutar pruebas con: `pytest`

### Cambios que Rompen Compatibilidad (Breaking Changes)
*   **Ninguno.** v2.0 está diseñado para ser **aditivo**. Los proyectos v1.0 existentes pueden adoptar estas herramientas incrementalmente.
*   *Nota:* Si eliges usar `ACTIVE.md`, debes seguir el esquema, de lo contrario `data_validator.py` reportará errores.

### Problemas Conocidos
*   **Fases 3 y 4 Incompletas**: La capa "Inteligente" (Preflight Inteligente, Generador de Prompts) falta.
*   **Sondeo del Vigilante**: La herramienta `watchdog_sync.py` actualmente depende del sondeo (polling) en algunos entornos si la biblioteca `watchdog` no está totalmente soportada.
*   **Escritura Manual de Specs**: Todavía tienes que escribir `specs/` manualmente; el generador de IA para specs llegará en la Fase 3.
