# Tópico 4: Seguimiento de Línea

## Experiencia 4.1 - Robustez del detector de carril

### Contexto semiaplicado
Antes del control autónomo, el equipo debe validar la calidad de detección de carril en distintos tramos del circuito.

### Objetivo
Evaluar cuándo el detector identifica correctamente carriles y cuándo pierde confianza.

### Preparación

```bash
ros2 launch my_qcar_nodes lane_detection.launch.py image_topic:=/qcar/csi_front/image_raw
ros2 topic echo /planning/lane_detected
ros2 topic echo /planning/center_offset
```

### Actividades
1. Seleccionar 5 zonas del circuito (rectas, curvas, intersecciones visuales).
2. Registrar para cada zona:
   - porcentaje aproximado de tiempo con `lane_detected=true`
   - variación de `center_offset`
3. Identificar patrones de fallo (sombra, color, geometría, ROI).
4. Proponer dos mejoras concretas del detector.

### Entregables
- Tabla de desempeño por zona.
- Catálogo de fallas observadas.
- Propuesta de mejoras priorizadas.

### Evaluación sugerida (100%)
- Cobertura de escenarios: 30%
- Calidad de evidencia: 35%
- Pertinencia de mejoras: 35%

---

## Experiencia 4.2 - Sintonía de controlador PD

### Contexto semiaplicado
Se necesita minimizar oscilaciones laterales manteniendo velocidad de operación útil.

### Objetivo
Sintonizar `kp` y `kd` en el seguidor de línea para mejorar estabilidad y tiempo de corrección.

### Preparación
Lanzar sistema integrado:

```bash
ros2 launch my_qcar_nodes lane_following_perception.launch.py image_topic:=/qcar/csi_front/image_raw base_velocity:=0.45
```

### Actividades
1. Definir una configuración base de `kp` y `kd`.
2. Ejecutar barrido de parámetros (al menos 6 combinaciones).
3. Medir indicadores:
   - oscilación lateral cualitativa
   - tiempo de recuperación tras curva
   - continuidad de avance sin detenciones por pérdida de carril
4. Elegir la mejor configuración y justificarla.

### Entregables
- Matriz de sintonía con resultados.
- Configuración recomendada final.
- Justificación técnica de compromiso estabilidad/rapidez.

### Evaluación sugerida (100%)
- Metodología de sintonía: 35%
- Calidad de comparación entre pruebas: 35%
- Argumentación final: 30%

---

## Experiencia 4.3 - Seguridad funcional por pérdida de carril

### Contexto semiaplicado
La industria exige comportamiento seguro ante fallo de percepción.

### Objetivo
Verificar la lógica fail-safe del seguidor cuando no hay detección reciente de carril.

### Preparación

```bash
ros2 launch my_qcar_nodes lane_following_perception.launch.py
ros2 topic echo /qcar/velocity_target
ros2 topic echo /qcar/steering_target
```

### Actividades
1. Forzar pérdida visual de carril en distintos momentos.
2. Medir tiempo aproximado hasta comando de detención.
3. Validar que el sistema no mantenga comando peligroso tras pérdida prolongada.
4. Proponer criterios de certificación básica para esta función de seguridad.

### Entregables
- Evidencia temporal de activación fail-safe.
- Evaluación de riesgo residual.
- Requisitos mínimos de seguridad propuestos.

### Evaluación sugerida (100%)
- Pruebas de fallo bien diseñadas: 40%
- Diagnóstico de seguridad: 35%
- Calidad de criterios propuestos: 25%
