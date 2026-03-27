# Tópico 1: Movimiento Simple del Auto

## Experiencia 1.1 - Calibración empírica de actuadores

### Contexto semiaplicado
El equipo de integración necesita una tabla de referencia entre comandos de control y respuesta del vehículo para una futura conducción autónoma.

### Objetivo
Estimar cómo cambia la trayectoria al modificar velocidad y steering, e identificar zonas de operación estables.

### Preparación
Ejecutar simulación y luego:

```bash
ros2 launch my_qcar_nodes basic_movement.launch.py
```

### Actividades
1. Editar parámetros en el launch o lanzar variantes con distintos valores de `velocity` y `steering`.
2. Probar al menos 9 combinaciones (3 velocidades x 3 direcciones).
3. Para cada combinación, medir:
   - Si el auto mantiene trayectoria estable.
   - Tendencia (recta, curva suave, curva cerrada).
   - Tiempo aproximado para desviarse de carril.
4. Construir un mapa operativo: combinaciones seguras y no seguras.

### Entregables
- Tabla de pruebas (9 o más casos).
- Mapa de operación recomendado.
- Breve análisis de por qué ciertos rangos son inestables.

### Evaluación sugerida (100%)
- Diseño experimental y cobertura de pruebas: 35%
- Calidad del registro de datos: 30%
- Análisis técnico y conclusiones: 35%

---

## Experiencia 1.2 - Respuesta transitoria ante cambios bruscos

### Contexto semiaplicado
Antes de desplegar un sistema de control superior, se debe verificar que cambios rápidos de referencia no provoquen maniobras peligrosas.

### Objetivo
Analizar el comportamiento transitorio del vehículo frente a escalones en velocidad y dirección.

### Preparación
Usar teleoperación:

```bash
ros2 launch my_qcar_nodes keyboard_teleop.launch.py
```

### Actividades
1. Definir tres secuencias de comandos tipo escalón (por ejemplo: recta -> giro -> recta).
2. Ejecutar cada secuencia 3 veces.
3. Registrar:
   - Tiempo subjetivo de establecimiento.
   - Sobreoscilación visible de la dirección.
   - Errores recurrentes (zig-zag, trompo, deriva).
4. Proponer límites de operación para conducción segura manual.

### Entregables
- Descripción de 3 secuencias de prueba.
- Resultados comparativos entre repeticiones.
- Reglas operativas de seguridad propuestas por el equipo.

### Evaluación sugerida (100%)
- Rigor de pruebas repetidas: 30%
- Identificación de riesgos dinámicos: 35%
- Recomendaciones justificadas: 35%

---

## Experiencia 1.3 - Puente de control: validación de consistencia

### Contexto semiaplicado
Un proveedor reporta inconsistencias entre los comandos publicados y la respuesta real del actuador en simulación.

### Objetivo
Validar el flujo completo `target -> bridge -> controladores` y detectar discrepancias.

### Preparación
Lanzar puente + movimiento:

```bash
ros2 launch my_qcar_nodes basic_movement.launch.py
```

Monitorear tópicos:

```bash
ros2 topic echo /qcar/velocity_target
ros2 topic echo /qcar/steering_target
ros2 topic echo /rl_controller/commands
ros2 topic echo /rr_controller/commands
```

### Actividades
1. Comparar valores enviados a `qcar_target` vs controladores de ruedas.
2. Verificar coherencia de signo y magnitud para avance y giro.
3. Repetir con al menos 4 configuraciones de entrada.
4. Escribir hipótesis de causa si hay comportamientos anómalos.

### Entregables
- Matriz de trazabilidad (entrada/salida por tópico).
- Diagnóstico de coherencia del bridge.
- Propuesta de mejora técnica.

### Evaluación sugerida (100%)
- Trazabilidad y evidencia: 40%
- Precisión del diagnóstico: 35%
- Calidad de propuesta de mejora: 25%
