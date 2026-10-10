# Cómo abrir el diagrama de clases en Lucidchart

Archivos en esta carpeta:

- `diagrama-clases.puml` — fuente UML (PlantUML), editable
- `diagrama-clases.svg` — vector (mejor para Lucidchart)
- `diagrama-clases.png` — imagen

Lucidchart **no abre `.puml` directo**. Usa una de estas vías.

## Opción A (recomendada): importar el SVG

1. Entra a [https://www.lucidchart.com](https://www.lucidchart.com) e inicia sesión.
2. **+ New** → **Lucidchart** → documento en blanco (o **UML**).
3. Menú **File → Import** (o arrastra el archivo).
4. Elige `diagrama-clases.svg`.
5. Si entra como imagen: clic derecho → **Ungroup** si Lucidchart lo permite.
   Si queda como una sola figura, úsala así en la diapositiva / sustentación (se ve nítida al hacer zoom).

## Opción B: pegar PlantUML y regenerar

1. Abre [https://www.plantuml.com/plantuml/uml](https://www.plantuml.com/plantuml/uml)
2. Pega el contenido de `diagrama-clases.puml`
3. **SVG** o **PNG** → descarga
4. En Lucidchart: **File → Import** esa imagen

## Opción C: dibujarlo en Lucidchart a mano (para editar cajas)

1. **+ New** → busca la plantilla **UML Class Diagram** / **Class**.
2. En la librería izquierda: **UML**.
3. Sigue los paquetes del `.puml`:
   - `domain.bingo` (Celda, Carton, Oraculo, patrones)
   - `domain.bots` (Bot y 4 rivales)
   - `domain.partida` (Partida)
   - `domain.campania` (Jugador, Campania, Recompensa)
   - `domain.boosters`
   - `domain.identidad` (Usuario, Administrador)
   - `application` (ComprarBooster, IniciarSesion)
   - `infrastructure` + tablas PostgreSQL

Herencia = flecha vacía (triángulo).  
Implementa interfaz = flecha punteada.  
Composición (♦ relleno): Carton–Celda, Partida–Oraculo.

## Qué mostrar al instructor

El diagrama cubre **todas las clases POO del juego y del backend**. Vue no son clases (Composition API); el dominio sí.
