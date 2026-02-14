# Contribuyendo a la Finalización de v2.0

## 🚧 Estado Actual
*   **Fase 1 y 2:** ✅ Completado (63% de la hoja de ruta total)
*   **Fase 3 y 4:** ⏳ Pendiente (37%)

Estamos buscando colaboradores para ayudarnos a cruzar la línea de meta mientras nuestro Arquitecto principal (Claude Opus) está en un descanso obligatorio (límite de cuota).

## Cómo Ayudar

### Opción 1: Implementar una Línea de Trabajo (La "Gran Ayuda")
Las Fases 3 y 4 están totalmente planificadas. Puedes tomar una pala y empezar a cavar inmediatamente.

**Líneas de Trabajo Disponibles (Ver `PLAN.md` para detalles):**
*   **[ ] Fase 3.1: Mejora de Preflight Inteligente**
    *   *Objetivo:* Construir `mission_analyzer.py` para recomendar habilidades basadas en `mission.md`.
*   **[ ] Fase 3.2: Cumplimiento de Estructura de Artefactos**
    *   *Objetivo:* Construir `artifact_manager.py` para hacer cumplir la estructura de la carpeta `artifacts/`.
*   **[ ] Fase 3.3: Generador de Prompts Inteligente**
    *   *Objetivo:* Construir `generate_worker_prompt.py` usando plantillas Jinja2.
*   **[ ] Fase 4.1: Documentación de Especificaciones**
    *   *Objetivo:* Escribir especificaciones formales para las herramientas Python.

**Cómo reclamar una línea de trabajo:**
1.  Revisa la pestaña de Issues (o `PLAN.md`) para asegurar que no esté reclamada.
2.  Lee la **Definición de Línea de Trabajo** en `PLAN.md`.
3.  Implementa la característica siguiendo el estilo de código en `.context/coding_style.md`.
4.  Escribe pruebas (obligatorio).
5.  Envía un PR.

### Opción 2: Probar y Dar Retroalimentación (La "Ayuda Estratégica")
Necesitamos datos del mundo real.
*   Usa `ACTIVE.md` en tu propio proyecto.
*   ¿Realmente ayuda? ¿Olvidas a menudo actualizarlo?
*   ¿Te ahorró tiempo `scaffold.py`?
*   Abre un Issue con tu experiencia. "Probé la Sincronización de Contexto y aquí es donde falló" es una retroalimentación extremadamente valiosa.

### Opción 3: Mejorar la Documentación (La "Ayuda Amistosa")
*   Nuestros docstrings son buenos, pero nuestros tutoriales son inexistentes.
*   Escribe una guía de "Cómo usé v2.0 para construir X".
*   Mejora la `MIGRATION_GUIDE` basada en tu experiencia de migración real.

## Configuración de Desarrollo

1.  **Clona el repo:**
    ```bash
    git clone https://github.com/nashishoo/antigravity-template-ide-native.git
    cd antigravity-template-ide-native
    ```

2.  **Instala Dependencias de Desarrollo:**
    ```bash
    pip install -r requirements.txt
    pip install pytest
    ```

3.  **Ejecuta Pruebas:**
    Asegúrate de que la línea base esté en verde antes de comenzar.
    ```bash
    pytest
    ```

## Estándares de Código
*   **Estilo:** Sigue `.context/coding_style.md`.
*   **Tipos:** Las sugerencias de tipo (Type hints) son **obligatorias** para todo el código Python nuevo.
*   **Validación:** Usa `pydantic` para modelos de datos.
*   **Pruebas:** Ninguna característica está "hecha" sin una prueba en `tests/`.

## Proceso de Revisión
*   Los PRs son revisados por el equipo central (actualmente Humanos + Agentes de IA).
*   Las pruebas automatizadas deben pasar.
*   Valoramos la **claridad** sobre la astucia.

## ¿Preguntas?
*   Abre un GitHub Issue.
*   Únete a la discusión en Discord (si aplica).
