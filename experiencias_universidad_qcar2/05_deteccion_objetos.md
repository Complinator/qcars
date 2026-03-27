# Tópico 5: Detección de Objetos

## Experiencia 5.1 - Curva de desempeño vs umbral de confianza

### Contexto semiaplicado
El equipo de percepción debe seleccionar un umbral de confianza óptimo para operación urbana simulada.

### Objetivo
Comparar desempeño de detección al variar `confidence_threshold`.

### Preparación

```bash
ros2 launch my_qcar_nodes object_detection.launch.py image_topic:=/qcar/csi_front/image_raw confidence_threshold:=0.45
ros2 topic echo /perception/object/detections
```

### Actividades
1. Ejecutar pruebas con umbral 0.30, 0.45 y 0.60.
2. En cada configuración, registrar:
   - número de detecciones totales
   - detecciones plausibles
   - posibles falsos positivos
3. Comparar sensibilidad y precisión cualitativa.
4. Recomendar umbral para escenario de seguridad.

### Entregables
- Tabla comparativa por umbral.
- Discusión de trade-off detección temprana vs falsas alarmas.
- Recomendación final justificada.

### Evaluación sugerida (100%)
- Calidad del experimento: 35%
- Análisis comparativo: 40%
- Recomendación técnica: 25%

---

## Experiencia 5.2 - Trazabilidad percepción -> decisión

### Contexto semiaplicado
El área de integración solicita garantizar que toda detección publicada pueda auditarse visualmente.

### Objetivo
Validar consistencia entre overlay visual y mensaje JSON de detecciones.

### Preparación

```bash
ros2 launch my_qcar_nodes object_detection.launch.py
```

### Actividades
1. Elegir 10 instantes de observación.
2. Para cada instante, contrastar:
   - cajas dibujadas en overlay
   - clase y confianza en JSON publicado
3. Detectar inconsistencias de etiqueta, caja o confianza.
4. Diseñar un checklist de auditoría de detección para uso en laboratorio.

### Entregables
- Matriz de consistencia overlay/JSON.
- Lista de inconsistencias encontradas.
- Checklist de auditoría propuesto.

### Evaluación sugerida (100%)
- Rigor de auditoría: 40%
- Calidad de evidencia: 35%
- Utilidad del checklist: 25%

---

## Experiencia 5.3 - Validación para operación mixta con seguimiento de línea

### Contexto semiaplicado
Se planea integrar detección de objetos con un comportamiento de guiado por carril.

### Objetivo
Evaluar convivencia de módulos de percepción simultáneos y su impacto en operación global.

### Preparación

```bash
ros2 launch my_qcar_nodes lane_following_perception.launch.py image_topic:=/qcar/csi_front/image_raw confidence_threshold:=0.50 base_velocity:=0.45
```

### Actividades
1. Observar simultáneamente overlays de carril y objetos.
2. Verificar continuidad de control de línea en presencia de múltiples detecciones.
3. Identificar degradación de desempeño (latencia visual, pérdida temporal, falsas detecciones).
4. Proponer arquitectura de priorización para futura toma de decisiones (por ejemplo: reducir velocidad ante clase de alto riesgo).

### Entregables
- Informe de integración multi-percepción.
- Riesgos técnicos detectados.
- Estrategia de priorización de decisiones.

### Evaluación sugerida (100%)
- Análisis de integración: 40%
- Detección de riesgos reales: 30%
- Calidad de arquitectura propuesta: 30%
