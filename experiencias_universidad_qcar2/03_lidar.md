# Tópico 3: Lidar

## Experiencia 3.1 - Mapa polar-cartesiano del entorno local

### Contexto semiaplicado
Un equipo de navegación necesita un mapa local rápido para maniobras de evasión.

### Objetivo
Interpretar datos de LaserScan y relacionarlos con posiciones relativas del entorno.

### Preparación

```bash
ros2 launch my_qcar_nodes lidar_visualizer.launch.py
```

### Actividades
1. Identificar en la visualización: frente del vehículo, laterales y zona trasera observable.
2. Ubicar 3 obstáculos visibles y estimar distancia relativa.
3. Comparar estimación visual con datos numéricos de `ranges`.
4. Discutir limitaciones de resolución angular y ruido.

### Entregables
- Esquema del entorno con obstáculos identificados.
- Comparación estimación visual vs dato numérico.
- Conclusión sobre confiabilidad de lectura.

### Evaluación sugerida (100%)
- Correcta interpretación geométrica: 40%
- Uso de evidencia cuantitativa: 30%
- Análisis de limitaciones: 30%

---

## Experiencia 3.2 - Detección de zona libre para avance

### Contexto semiaplicado
Se requiere una regla simple para decidir si avanzar o frenar según ocupación frontal.

### Objetivo
Diseñar una métrica de seguridad frontal usando sector angular y distancia mínima.

### Preparación

```bash
ros2 launch my_qcar_nodes lidar_visualizer.launch.py
ros2 topic echo /qcar/scan
```

### Actividades
1. Definir sector frontal (por ejemplo, +-20 grados).
2. Calcular distancia mínima y media del sector para distintos escenarios.
3. Proponer regla de decisión:
   - Avanzar si distancia minima > d_segura.
   - Reducir velocidad o detener en caso contrario.
4. Evaluar falsas alarmas y detecciones tardías.

### Entregables
- Definición formal de métrica de seguridad.
- Resultados en al menos 5 escenarios.
- Discusión de trade-off seguridad vs fluidez.

### Evaluación sugerida (100%)
- Formulación de métrica: 35%
- Validación experimental: 35%
- Calidad de análisis de trade-off: 30%

---

## Experiencia 3.3 - Perfilado de percepción en tiempo real

### Contexto semiaplicado
Se necesita saber si el pipeline lidar puede sostener decisiones a alta frecuencia.

### Objetivo
Evaluar carga computacional y comportamiento temporal del visualizador lidar.

### Preparación

```bash
ros2 launch my_qcar_nodes lidar_visualizer.launch.py
ros2 topic hz /qcar/scan
```

### Actividades
1. Medir frecuencia de entrada del scan.
2. Observar respuesta visual bajo carga (más obstáculos o escenas complejas).
3. Determinar si hay degradación visible o atraso.
4. Proponer optimizaciones (filtrado, submuestreo, límites de distancia).

### Entregables
- Registro de rendimiento percibido.
- Diagnóstico de cuellos de botella.
- Plan de optimización priorizado.

### Evaluación sugerida (100%)
- Evidencia de rendimiento: 30%
- Diagnóstico técnico: 40%
- Calidad de propuestas: 30%
