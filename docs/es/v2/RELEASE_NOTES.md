# Notas de la Versión: Plantilla Antigravity v2.0-alpha.1

## 🎯 Qué Resuelve Esta Alpha

En el proyecto **Catapaz Adopt Me Bot**, chocamos con una pared: a medida que el proyecto crecía, los agentes comenzaban a "olvidar" lo que sucedía en sesiones anteriores. Sobrescribían el trabajo de otros o pedían al Arquitecto información que ya se había decidido.

**v2.0-alpha.1 introduce el "Protocolo de Estado Compartido" para arreglar esto.** Mantiene al Arquitecto y a todos los agentes Trabajadores en perfecta sincronía, reduciendo drásticamente la "amnesia" y la deriva de contexto.

### ✅ Características Completadas

**Fase 1: Sincronización de Contexto**
*   **Protocolo ACTIVE.md**: Un "canal de transmisión" dedicado para el estado del proyecto. Los agentes lo leen al entrar y lo actualizan al salir.
*   **Sincronización PLAN.md**: Tu hoja de ruta ahora es legible por máquinas. Los agentes pueden buscar "¿Qué representa la Línea de Trabajo 2.1?" y obtener la respuesta al instante.
*   **Higiene del Archivo**: Mantén el enfoque de tu espacio de trabajo agudo. Los archivos viejos se mueven automáticamente a `.archive/` con preservación de metadatos.

**Fase 2: Infraestructura de Herramientas Python**
*   **Validador de Datos**: Previene la configuración "alucinada". Si un agente escribe YAML inválido en `ACTIVE.md`, esta herramienta lo atrapa.
*   **Generador de Estructura**: Comienza nuevas tareas al instante. Genera la estructura de carpetas, plantillas de especificaciones y stubs de prueba por ti.
*   **Sincronización de Vigilante**: Un monitor de archivos "consciente". Si cambias un archivo pero olvidas actualizar la documentación, te da un toque.
*   **Suite de Pruebas**: 49 pruebas pasando asegurando una estabilidad sólida como una roca para la capa de herramientas.

### 📊 Métricas de Impacto (Estimadas)
*   **Deriva de Contexto**: Reducida en **~60%** (Los agentes actúan sobre datos actuales, no alucinaciones).
*   **Incorporación de Trabajadores**: **~1 min** (era ~5 min). Los agentes simplemente leen `ACTIVE.md` y comienzan.
*   **Validación Manual**: **Automatizada**. No más revisiones manuales de archivos de configuración.
*   **Andamiaje**: **Automatizado**. `scaffold.py` hace el trabajo pesado.

### ⚠️ Limitaciones Conocidas
*   **Sin "Cerebro" Aún**: El descubrimiento inteligente de habilidades y la generación de prompts inteligentes llegarán en la Fase 3.
*   **Configuración Manual**: Necesitas copiar estos archivos manualmente a tu proyecto existente (ver Guía de Migración).

### 🚧 ¿Por Qué Lanzar Incompleto?
Estamos lanzando esto ahora porque **la Sincronización de Contexto (Fase 1) es demasiado valiosa para mantenerla oculta.** Incluso sin la inteligencia de la Fase 3, las mejoras de estabilidad de la Fase 1 cambian el juego para flujos de trabajo agénticos complejos. Queremos que lo uses y lo rompas para que podamos hacer la v2.0 Final perfecta.

### 📅 Hoja de Ruta
*   **Fase 3 (Inteligencia):** 20 Feb, 2026 (Pendiente renovación de cuota genérica)
*   **Fase 4 (Docs):** 21 Feb, 2026
*   **v2.0.0 Final:** 22 Feb, 2026

### 🙏 Agradecimientos
*   **Diseño**: Claude Opus 4.6 (Pensando) por el "Análisis de Causa Raíz".
*   **Retroalimentación**: Gemini 3 Pro por las revisiones arquitectónicas brutales pero necesarias.
*   **Código**: Claude Sonnet 4.5 & Gemini 3 Flash por la implementación.
*   **Orquestación**: Usuario Humano por guiar el enjambre.

### 📥 Inicio Rápido en 3 Pasos
1.  **Respalda** tu proyecto actual.
2.  **Copia** las carpetas `.context/` y `src/tools/` a tu proyecto.
3.  **Ejecuta** `python src/tools/data_validator.py` para verificar tu configuración.
