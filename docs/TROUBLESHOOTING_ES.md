# 🔧 Guía de Solución de Problemas

## El Flujo "Parallel Architect"

### 1. "Mis workers están perdidos / alucinando."
**Causa:** Mala Inyección de Contexto.
**Solución:** Asegúrate de que cada prompt de worker comience con el **Bloque de Contexto**:
```markdown
## CONTEXT
- Project: [Nombre]
- Stack: IDE-Native
- Tooling: `src/skills/` (planning-with-files)
```
Sin esto, el agente no sabe que es parte de un sistema mayor.

### 2. "No sé qué hacer después."
**Causa:** Falta `task_plan.md`.
**Solución:** Pídele a tu Arquitecto (Ventana Principal) que:
> "Inicializa el archivo `task_plan.md` usando la skill `planning-with-files`."
Este archivo se convierte en el GPS de tu proyecto.

### 3. "El agente intenta ejecutar código Python y falla."
**Causa:** Fantasma del motor antiguo.
**Solución:** Recuérdale al agente:
> "Eres un agente IDE-Native. No intentes ejecutar scripts de python directamente a menos que estén en `src/tools/`. Usa tus herramientas internas (edit_file, run_terminal) en su lugar."

### 4. "¿Cómo instalo nuevas skills?"
**Causa:** Confusión sobre `skills.sh`.
**Solución:** Usa la terminal en cualquier ventana:
```bash
npx skills search [query]
npx -y skills add [nombre-skill]
```
Luego dile al agente: "Instalé [skill]. Revisa `src/skills/`."

## Errores Comunes

### `Element type is invalid...` (React)
- **Check:** ¿Estás importando un export por defecto como nombrado?
- **Solución:** Revisa `import X from './X'` vs `import { X } from './X'`.

### `Git push failed`
- **Check:** ¿Configuraste tu identidad?
- **Solución:**
  ```bash
  git config user.name "Tu Nombre"
  git config user.email "tu@email.com"
  ```
