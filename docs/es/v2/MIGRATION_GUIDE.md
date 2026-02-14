# Guía de Migración: v1.0 → v2.0-alpha

## ¿Deberías Actualizar Ahora?

v2.0-alpha es **aditiva**, lo que significa que añade nuevas capacidades sin romper los flujos de trabajo v1.0 existentes. Sin embargo, introduce más estructura.

### ✅ Actualiza si:
*   **Experimentas "Deriva de Contexto":** Los agentes olvidan constantemente lo que se decidió en turnos anteriores.
*   **Pierdes el rastro del estado:** Editas manualmente un `status.txt` o simplemente lo mantienes en tu cabeza.
*   **Validas manualmente:** Te encuentras arreglando encabezados YAML rotos o archivos JSON a mano.
*   **Odias el código repetitivo:** Quieres generar estructuras de herramientas automáticamente.

### ⏳ Espera a v2.0 Final si:
*   **Quieres magia:** Estás esperando el "Generador de Prompts Inteligente" y el "Preflight Inteligente" (Fase 3).
*   **Necesitas documentación perfecta:** La documentación es actualmente escasa (alpha).
*   **Estás a medio sprint:** Si estás en medio de una característica crítica, termínala primero.

## Qué Cambió (Alto Nivel)

### Nuevos Archivos (Seguro de Añadir)
*   `.context/ACTIVE.md`: **Altamente Recomendado.** El nuevo cerebro de tu proyecto.
*   `src/tools/*`: Una suite de 5 nuevas herramientas Python para automatización.
*   `.archive/`: Una estructura de carpetas para limpieza.
*   `tests/`: Pruebas unitarias para las nuevas herramientas.

### Archivos Modificados
*   **Ninguno.** No hemos modificado ningún archivo central de v1.0 de manera disruptiva.
*   *Nota:* `PLAN.md` tiene un esquema más estricto si quieres usar `plan_sync.py`, pero tu viejo `PLAN.md` esencialmente será ignorado por la herramienta hasta que lo actualices.

### Nuevas Dependencias
*   `pyyaml`: Requerido para analizar `ACTIVE.md`.
*   `pydantic`: Requerido para `data_validator.py` (validación de esquemas).
*   `pytest`: Requerido para ejecutar la suite de pruebas.
*   `watchdog` (Opcional): Para la herramienta de vigilancia de archivos.

## Migración Paso a Paso

### 1. Respalda Tu Proyecto
Siempre ve a lo seguro.
```bash
git checkout -b backup-before-v2
# o simplemente comprime tu carpeta del proyecto
```

### 2. Añade Archivos v2.0 (No Destructivo)
Copia los siguientes directorios de la plantilla v2.0 a la raíz de tu proyecto:
*   `.context/`
*   `.archive/`
*   `src/tools/`
*   `tests/`
*   `specs/` (específicamente `active_context_protocol.md`)

*Consejo: NO sobrescribas tu `PLAN.md` o `mission.md` existente todavía.*

### 3. Inicializa ACTIVE.md
Crea `.context/ACTIVE.md` si no lo copiaste. Puedes usar la plantilla en `specs/active_context_protocol.md`. Este archivo comenzará inmediatamente a servir como la "Fuente de la Verdad" para cualquier agente que sepa buscarlo.

### 4. Instala Dependencias
Crea o actualiza tu `requirements.txt` / `pyproject.toml`:
```text
pyyaml>=6.0
pydantic>=2.0
pytest>=7.0
watchdog>=3.0  # Opcional
```
Instálalas:
```bash
pip install -r requirements.txt
```

### 5. Valida la Instalación
Ejecuta el validador para asegurar que todo esté configurado correctamente:
```bash
python src/tools/data_validator.py
```
Debería reportar "Validation Successful" (o decirte si faltan campos en `ACTIVE.md`).

## Plan de Reversión (Rollback)
Si decides que v2.0 aún no es para ti:
1.  Elimina `.context/ACTIVE.md`
2.  Elimina `src/tools/` (o estrictamente los archivos nuevos)
3.  Elimina `.archive/`
4.  Tu proyecto vuelve al estándar v1.0.

## FAQ (Preguntas Frecuentes)

**P: ¿Seguirán funcionando mis trabajadores existentes?**
R: **Sí.** Los protocolos v2.0 son "optativos". Si un trabajador no busca `ACTIVE.md`, simplemente funciona como lo hacía antes (con las mismas limitaciones de contexto).

**P: ¿TENGO que usar ACTIVE.md?**
R: **No**, pero lo recomendamos encarecidamente. Es el mecanismo que evita que los agentes alucinen el estado del proyecto.

**P: ¿Puedo usar las herramientas sin los protocolos?**
R: Mayormente sí. `scaffold.py` funciona de forma independiente. `archive_manager.py` funciona de forma independiente. `plan_sync.py` requiere que `PLAN.md` siga el nuevo esquema.
