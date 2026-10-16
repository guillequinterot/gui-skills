# Proyectos y marcas

Un archivo por proyecto o marca (`<caso-código>.md`) con valores y decisiones **solo de ese proyecto**: colores, tipografías, componentes, excepciones aprobadas, referencia al Figma (por nombre, nunca con enlaces ni ids de cuentas ajenas) y, si el usuario usa Obsidian, a su nota de proyecto.

Reglas:

- El archivo se nombra con el **código de caso** (`caso-<tipo>-<NN>`); nunca con el nombre del cliente. La equivalencia código → cliente vive en `~/.gui-skills/equivalencias.md`, fuera del repo.
- Nada de aquí se convierte en regla global sin aprobación explícita.
- La fuente de verdad de estilos es el **Figma del proyecto**; este archivo es un resumen para trabajar rápido y debe verificarse contra Figma.
- Decisiones de gestión (pendientes, entregables, fechas) van en la carpeta del proyecto del usuario y, si usa Obsidian, en la nota del proyecto de su vault (`obsidian_projects_folder`).

Plantilla mínima:

```markdown
# <caso-código>
- Tipo de cliente/marca (genérico):
- Figma (Styles/Variables):
- Nota de Obsidian (opcional):
- Colores (nombre de estilo → valor):
- Tipografías (estilo → familia/tamaño/peso/lh):
- Componentes existentes en Figma:
- Excepciones aprobadas al método (fecha, motivo):
```

Índice de casos: ver **`INDICE.md`**.
