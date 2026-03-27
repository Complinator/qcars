# Tópico 2: Cámara

## Experiencia 2.1 - Caracterización del flujo de imagen

### Contexto semiaplicado
El equipo de percepción requiere conocer la robustez del stream de cámara para alimentar módulos de visión en tiempo real.

### Objetivo
Medir estabilidad del tópico de imagen y su impacto en visualización y procesamiento.

### Preparación

```bash
ros2 launch my_qcar_nodes camera_visualizer.launch.py
```

Comandos de verificación:

```bash
ros2 topic hz /qcar/csi_front/image_raw
ros2 topic bw /qcar/csi_front/image_raw
```

### Actividades
1. Medir frecuencia durante 3 ventanas de 60 s.
2. Estimar variabilidad de tasa y discutir causas.
3. Identificar eventos de congelamiento o pérdida visual.
4. Definir requisitos mínimos para percepción estable (fps y continuidad).

### Entregables
- Tabla de frecuencia/ancho de banda.
- Evidencia de estabilidad o inestabilidad.
- Requisitos técnicos propuestos.

### Evaluación sugerida (100%)
- Calidad de medición: 35%
- Interpretación de resultados: 35%
- Recomendaciones técnicas: 30%

---

## Experiencia 2.2 - Sensibilidad a cambios de escena

### Contexto semiaplicado
Se desea validar si la cámara permite detectar condiciones de riesgo visual en escenarios con texturas variables.

### Objetivo
Evaluar sensibilidad de la imagen ante variaciones de contraste, ángulo y oclusión parcial.

### Preparación

```bash
ros2 launch my_qcar_nodes camera_visualizer.launch.py
```

### Actividades
1. Diseñar 4 escenas en Gazebo (recta limpia, curva, textura compleja, oclusión parcial).
2. Para cada escena, registrar:
   - Legibilidad visual de carriles.
   - Presencia de ruido o artefactos.
   - Posibles fallas para módulos de percepción.
3. Clasificar cada escena por dificultad (baja/media/alta).
4. Proponer preprocesamiento mínimo recomendado.

### Entregables
- Matriz de escenas y dificultad.
- Diagnóstico de calidad visual por escena.
- Propuesta de preprocesamiento (HSV, umbrales, ROI, etc.).

### Evaluación sugerida (100%)
- Diseño de casos de prueba: 30%
- Profundidad de análisis visual: 40%
- Viabilidad de mejora propuesta: 30%

---

## Experiencia 2.3 - Validación de QoS para sensores simulados

### Contexto semiaplicado
El sistema integrado presenta pérdidas intermitentes y se sospecha incompatibilidad de QoS entre publicador y suscriptor.

### Objetivo
Comprobar el impacto de QoS en recepción de imágenes para simulación ROS2.

### Preparación
Usar la visualización de cámara y revisar configuración QoS del nodo.

### Actividades
1. Identificar el perfil QoS activo en el visualizador.
2. Explicar por qué `BEST_EFFORT` y `VOLATILE` suelen funcionar en sensores simulados.
3. Proponer y documentar un experimento controlado cambiando hipótesis de QoS.
4. Argumentar configuración final recomendada para el curso.

### Entregables
- Informe técnico de QoS (no solo observación, también justificación).
- Riesgos de usar perfiles no compatibles.
- Configuración recomendada y criterios de aceptación.

### Evaluación sugerida (100%)
- Comprensión de QoS: 40%
- Solidez de la argumentación: 35%
- Claridad técnica del informe: 25%
