# Taller Reloj - Estructuras de Datos

Reloj análogo y digital hecho únicamente con Python, **sin ninguna librería ni import**. Todo está en un solo archivo (`reloj.py`). La interfaz es una **ventana dibujada en la consola**, con barra de título, paneles y botones. Como funcionalidad adicional tiene un cronómetro con registro de vueltas.

**Estudiante:** Santiago Campoverde
**Asignatura:** Estructuras de Datos - Universidad Cooperativa de Colombia

## Cómo ejecutarlo

1. Abrir la carpeta del proyecto en **VS Code**
2. Abrir `reloj.py` y presionar ▶ (**Run Python File**), o escribir en la terminal:
   ```bash
   python reloj.py
   ```
3. Ingresar la hora inicial. El reloj empieza a andar solo y se redibuja en el mismo lugar, sin parpadear.
4. Presionar **Ctrl+C** para detenerlo y usar los botones.

Si el segundero va más rápido o más lento que un reloj real, se ajusta una vez con el botón `K`. Se recomienda la terminal de VS Code o Windows Terminal, porque el CMD clásico de Windows no muestra los colores.

## La ventana

```
+============================================================================+
| RELOJ CIRCULAR  -  Listas circulares dobles               Tema: Medianoche |
+---------------------------------------------+------------------------------+
|                . . .12 . . .                | HORA DIGITAL                 |
|           11 .               . 1            | 11:59:58 p. m.               |
|          .        +              .          | Formato: 12 horas            |
|       . .         +  *            . .       |                              |
|      .            ++ *               .      | MANECILLAS EN LAS LISTAS     |
|    10              + *                2     | Horas    22 <- [23] -> 00    |
|    .               + #                 .    | Minutos  58 <- [59] -> 00    |
|   .                 +#                  .   | Segundos 57 <- [58] -> 59    |
|  .                  +#                   .  |  anterior <- actual -> sig.  |
|  9                   @                   3  | CRONOMETRO                   |
|                     ...                     | ...                          |
+---------------------------------------------+------------------------------+
| [A] Avanzar  [R] Retroceder  [H] Ajustar hora  [M] En marcha  [F] 12/24h   |
| [C] Cronometro [E] Estructura [P] Pruebas [K] Calibrar [T] Tema [S] Salir  |
+----------------------------------------------------------------------------+
| Bienvenido. Escribe la letra de un boton y presiona Enter.                 |
+============================================================================+
```

- **Izquierda:** el reloj análogo, con la manecilla de la hora (`#`), la de los minutos (`*`) y la de los segundos (`+`). Debajo va la hora digital en números grandes.
- **Derecha:** la hora, el formato, el nodo actual de cada lista con su `prev` y su `next`, el estado del cronómetro y el último movimiento de los punteros.
- **Abajo:** los botones, que se usan escribiendo la letra y presionando Enter, y la barra de mensajes.

## Pantallas y botones

### Reloj (pantalla principal)
| Botón | Acción |
|---|---|
| `A` / `R` | Avanzar o retroceder segundos o minutos |
| `H` | Ajustar la hora |
| `M` | Poner el reloj en marcha: avanza solo, segundo a segundo (en la terminal del PC corre hasta presionar Ctrl+C) |
| `F` | Cambiar entre 12 y 24 horas |
| `C` | Ir al cronómetro |
| `E` | Ir a la estructura de la lista |
| `P` | Ejecutar las pruebas de funcionamiento |
| `K` | Calibrar el reloj en marcha con el cronómetro del celular |
| `T` | Cambiar el tema de color (Medianoche, Océano o Bosque) |
| `S` | Salir |

### Estructura
Muestra los tres anillos (horas, minutos y segundos) con `head`, el último nodo, `ultimo.next` y los vecinos del nodo actual.
- `N` mueve el segundero con `next` y `B` lo mueve con `prev`, explicando qué pasa con el minuto y la hora cuando se da la vuelta.
- `H` ajusta la hora y `X` vuelve al reloj.

### Cronómetro con vueltas (funcionalidad adicional)
- `I` inicia o pausa el cronómetro, `V` marca una vuelta y `A` avanza el tiempo.
- `>` y `<` recorren las vueltas con `next` y `prev`.
- `D` elimina la vuelta seleccionada, `Z` reinicia y `X` vuelve al reloj.
- También muestra la vuelta más rápida y la más lenta.

### Pruebas
Ejecuta 40 pruebas y las muestra en dos columnas con `OK` o `FALLO`.

## Uso de la lista circular doble

| Dónde se usa | Cómo se usa |
|---|---|
| Segundos, minutos y horas | Son tres anillos de 60, 60 y 24 nodos. El segundo se mueve con `next`; cuando vuelve a 0 avanza el minuto, y cuando el minuto vuelve a 0 avanza la hora. |
| Retroceder el tiempo | Se usa `prev`. Desde 00:00:00 se pasa a 23:59:59 porque la lista es circular. |
| Carátula del reloj | Las marcas y los números se dibujan recorriendo los 60 nodos del anillo de segundos hasta volver a `head`. |
| Vueltas del cronómetro | Cada vuelta se agrega con `insert_at_end`, y `>` y `<` se mueven con `next` y `prev`. De la última vuelta se pasa a la primera. |
| Formato 12 / 24 horas | Los formatos forman un anillo y cada cambio avanza con `next`. |
| Temas de color | Los temas (Medianoche, Océano y Bosque) forman un anillo y el botón `T` avanza con `next`. |

## Explicación del código

### `Node`
Es cada elemento de la lista. Guarda el valor (`data`) y dos punteros: `prev` apunta al nodo anterior y `next` al siguiente.

### `CircularDoublyLinkedList`
Es la lista circular doble hecha a mano. Guarda `head` (el primer nodo) y `size` (cuántos nodos tiene).

| Método | Qué hace |
|---|---|
| `insert_at_beginning(data)` | Crea un nodo antes de `head` y lo vuelve el nuevo `head`. |
| `insert_at_end(data)` | Crea un nodo después del último y lo conecta de nuevo con `head`. |
| `delete(data)` / `delete_node(node)` | Quita un nodo uniendo su anterior con su siguiente. Si era `head`, el siguiente pasa a ser `head`. |
| `find(data)` | Recorre la lista desde `head` hasta volver a `head` buscando el valor. |
| `to_list()` / `print_list()` | Recorren la lista una vez completa. |
| `is_empty()` / `clear()` | Revisan si la lista está vacía o la vacían. |

### `Clock`
Es el reloj. Tiene tres anillos (`hours`, `minutes` y `seconds`) y un puntero al nodo actual de cada uno.

| Método | Qué hace |
|---|---|
| `build_ring(amount)` | Crea un anillo con los números de 0 hasta `amount - 1`. |
| `set_time(h, m, s)` | Busca en cada anillo el nodo de la hora indicada y lo deja como actual. |
| `tick()` | Avanza un segundo con `next`, con el efecto en cadena sobre el minuto y la hora. Guarda la explicación de cada paso en `last_steps`. |
| `tick_back()` | Retrocede un segundo con `prev`. |
| `change_format()` | Cambia entre 12 y 24 horas. |
| `text()` / `short_text()` | Devuelven la hora como texto. |

### `Stopwatch` y `Lap`
`Lap` guarda el número, el tiempo parcial y el tiempo total de una vuelta. `Stopwatch` guarda las vueltas en una lista circular doble y un puntero `selected` a la vuelta seleccionada.
- `toggle()` inicia o pausa el cronómetro.
- `advance()` y `go_back()` suman o restan tiempo cuando el reloj avanza o retrocede.
- `add_lap()` registra una vuelta.
- `next_lap()` y `previous_lap()` mueven la selección.
- `delete_selected()` elimina la vuelta seleccionada.
- `best_lap()` y `worst_lap()` encuentran la vuelta más rápida y la más lenta.
- `reset()` reinicia el cronómetro.

### `Pacer`
Hace que el reloj en marcha avance solo, porque sin imports no existe `time.sleep`.
- `wait_one_second()` repite un ciclo vacío tantas veces que tarda aproximadamente un segundo.
- `adjust()` corrige la velocidad con una regla de tres a partir de la calibración.

### `AnalogFace`
Dibuja la carátula en una cuadrícula de 21 filas por 43 columnas. Recorre el anillo de segundos para poner las marcas y los números, y traza las manecillas con seno y coseno. Las funciones `sine` y `cosine` están hechas con la serie de Taylor, porque no se puede importar `math`.

### `Window`
Construye la ventana como una lista de líneas de texto: borde superior, barra de título, cuerpo dividido en dos paneles, botones, barra de mensajes y borde inferior. Todas las líneas tienen exactamente el mismo ancho, y hay dos pruebas que lo revisan en las tres pantallas, con colores y en texto simple. Los bordes son de línea doble (`╔ ═ ╗ ║`).

### `Painter` y `Theme`
Se encargan de los colores y de borrar la pantalla, usando códigos de escape ANSI, que son texto especial dentro de un `print`. Los temas están guardados en una lista circular doble.

### `App`
Es la aplicación.
- Guarda en qué pantalla se está (reloj, estructura o cronómetro).
- `clock_screen()`, `structure_screen()`, `stopwatch_screen()` y `tests_screen()` arman cada pantalla.
- `clock_action()`, `structure_action()` y `stopwatch_action()` ejecutan el botón elegido.
- `start()` es el ciclo principal: dibuja la ventana, lee un botón y repite.

### `Tester`
Ejecuta las 40 pruebas y guarda cada resultado. Revisa:
- **La lista:** insertar, buscar, eliminar y los enlaces circulares.
- **El reloj:** el cambio de minuto, el cambio de hora, la medianoche hacia adelante y hacia atrás, y los formatos.
- **El cronómetro:** las vueltas, la más rápida y la más lenta, el recorrido circular, eliminar y reiniciar.
- **El dibujo:** la carátula, que todos los bordes de la ventana queden alineados y la calibración.

### Validaciones
- `read_int` acepta solo números dentro del rango indicado.
- `read_option` acepta solo una de las letras de los botones.
- Si se escribe algo inválido, el programa avisa y vuelve a preguntar.

## Guion para la presentación

0. **Correrlo en VS Code:** el reloj arranca andando solo. Presiona **Ctrl+C** para ver los botones.
1. **`P`, pruebas:** muestra que las 40 salen en `OK`.
2. **`H`:** pon la hora en `23:59:58`.
3. **`E`, estructura:** explica `head`, el último nodo y que `ultimo.next` vuelve a `head`.
4. **`N` tres veces:** se ve cómo el segundo, el minuto y la hora dan la vuelta hasta `00:00:01`.
5. **`B` tres veces:** con `prev` vuelve a `23:59:58`.
6. **`X` y luego `M`:** pon el reloj en marcha otra vez y detenlo con Ctrl+C.
7. **`C`, cronómetro:** inícialo con `I`, avanza el tiempo con `A`, marca vueltas con `V` y recórrelas con `>` y `<`.

## Posibles preguntas del profesor

**¿Cómo hay una ventana si no se usó ninguna librería?**
La ventana está dibujada con caracteres (`+`, `-`, `|`) usando solo `print`. La clase `Window` arma cada línea con el mismo ancho para que los bordes queden alineados.

**¿Por qué una lista circular doble?**
Porque el reloj es circular: después del 59 viene el 00 y antes del 00 está el 59. Con `next` el reloj avanza y con `prev` retrocede, sin tener que validar los límites.

**¿Por qué la hora se ingresa a mano?**
Porque sin imports Python no puede leer la hora del computador. Para eso se necesitaría `time` o `datetime`.

**¿Cómo se detiene el reloj con Ctrl+C sin librerías?**
Ctrl+C hace que Python lance la excepción `KeyboardInterrupt`, que es parte del lenguaje y no necesita import. El programa la atrapa con `try` / `except` y muestra los botones.

**¿Cómo avanza solo el reloj en marcha sin `time.sleep`?**
Con un ciclo que se repite muchas veces y tarda aproximadamente un segundo. Como cada computador tiene una velocidad diferente, está la opción de calibrar.

**¿Cómo se dibujan las manecillas sin `math`?**
El seno y el coseno se calculan con la serie de Taylor. Con ellos se ubica cada punto de la manecilla según su ángulo: 6 grados por segundo o minuto, y 30 grados por hora.
