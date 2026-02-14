# 🚀 Plantilla de Espacio de Trabajo Antigravity v2.0-alpha

> [!WARNING]
> **LANZAMIENTO ALPHA - 63% COMPLETADO**
> Este es un lanzamiento funcional pero incompleto. Contiene la **infraestructura central** (Fases 1 y 2) pero carece de la **capa de guía inteligente** (Fases 3 y 4). Úselo con precaución.

## 📊 Estado Actual

| Fase | Componente | Estado | Completado |
|------|------------|--------|------------|
| **1** | **Sincronización de Contexto** | ✅ **Listo** | **100%** |
| **2** | **Infraestructura de Herramientas Python** | ✅ **Listo** | **100%** |
| 3 | Descubrimiento y Guía Mejorados | ⏳ Pendiente | 0% |
| 4 | Documentación e Integración | ⏳ Pendiente | 0% |

## 🚀 Qué Funciona (La "Carne")

Los cimientos de la arquitectura "Nativa Agente" están construidos y probados (49/49 pruebas pasando).

### Fase 1: Sincronización de Contexto
*   **Protocolo `.context/ACTIVE.md`**: Un archivo de estado especializado que elimina la deriva de contexto entre agentes trabajadores. Funciona como un tablero de memoria de "lectura-al-entrar, actualización-al-salir".
*   **Sistema de Sincronización `PLAN.md`**: Una hoja de ruta centralizada que rastrea las líneas de trabajo. Los trabajadores ahora pueden leer programáticamente el plan para entender su misión exacta.
*   **Higiene del Archivo**: Herramientas automatizadas para mover el trabajo completado a `.archive/`, manteniendo el espacio de trabajo activo limpio y las ventanas de contexto de los agentes enfocadas.

### Fase 2: Infraestructura de Herramientas Python
*   **Validación de Datos (`data_validator.py`)**: Motor de validación basado en Pydantic para `ACTIVE.md`, `PLAN.md` y otros archivos críticos. No más encabezados YAML rotos.
*   **Generador de Estructura (`scaffold.py`)**: Automatiza la creación de nuevas herramientas, especificaciones y estructuras básicas de archivos basadas en plantillas.
*   **Vigilante de Archivos (`watchdog_sync.py`)**: (Alpha) Monitorea cambios en archivos y sugiere actualizaciones a `ACTIVE.md` para mantener la documentación sincronizada con el código.

## 🚧 Qué Está Pendiente (Fases 3 y 4)

Actualmente estamos bloqueados por la **cuota de API de Claude Opus 4.6** (se espera la renovación en ~7 días).

*   **Preflight Inteligente**: La herramienta `mission_analyzer.py` que lee su `mission.md` y recomienda las habilidades exactas que necesita aún no está construida.
*   **Generador de Prompts Inteligente**: La herramienta para autogenerar prompts de trabajadores conscientes del contexto está pendiente.
*   **Documentación Profunda**: Las guías detalladas para cada herramienta todavía se están escribiendo.

## 🔮 ¿Por Qué Lanzar Incompleto?

Creemos en la **transparencia radical**. Este proyecto en sí es un caso de estudio vivo en desarrollo "Nativo Agente".

1.  **Transparencia**: Puedes ver exactamente cómo evoluciona un sistema arquitectado por IA.
2.  **Retroalimentación Temprana**: Queremos que pruebes el protocolo de **Sincronización de Contexto** (Fase 1) ahora. Resuelve el mayor punto de dolor del desarrollo agéntico: la *amnesia*.
3.  **Ayuda de la Comunidad**: Realmente necesitamos ayuda para completar las Fases 3 y 4 (ver `CONTRIBUTING_v2_ES.md`).

## 🚦 ¿Puedo Usar Esto Ahora?

Usa esta matriz simple para decidir:

| Hito | Usa v2.0-alpha SI... | Espera a v2.0-final SI... |
|------|----------------------|---------------------------|
| **Estabilidad** | Te sientes cómodo con la etiqueta "alpha" | Necesitas un producto terminado y sólido como una roca |
| **Punto de Dolor** | Luchas con la **Deriva de Contexto** (agentes olvidando cosas) | Luchas con el **Descubrimiento** (no sabes qué herramientas usar) |
| **Nivel de Habilidad** | Te sientes cómodo leyendo código Python | Necesitas tutoriales paso a paso para todo |

## 📅 Hoja de Ruta hacia v2.0 Final

| Hito | ETA | Notas |
|------|-----|-------|
| **Inicio Fase 3** | 20 Feb, 2026 | Dependiente de la renovación de cuota de Opus |
| **Inicio Fase 4** | 21 Feb, 2026 | Documentación y limpieza |
| **v2.0 Beta** | 22 Feb, 2026 | Funcionalidad completa, buscando testers |
| **v2.0 Final** | 24 Feb, 2026 | Lanzamiento estable |

## 🤝 Cómo Contribuir

Ver [CONTRIBUTING_v2_ES.md](CONTRIBUTING_v2_ES.md) para una lista de líneas de trabajo disponibles. ¡Tenemos especificaciones detalladas para los componentes de la Fase 3 listas para ser implementadas!

## 🎖️ Créditos

Esta evolución es una colaboración biológico-digital:
*   **Arquitectura**: Claude Opus 4.6 (Pensando)
*   **Implementación**: Claude Sonnet 4.5 & Gemini 3 Flash
*   **Aseguramiento de Calidad y Documentación**: Gemini 3 Pro
*   **Orquestación**: Usuario Humano
