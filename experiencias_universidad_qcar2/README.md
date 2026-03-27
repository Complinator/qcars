# Experiencias Universitarias QCar2 (Nivel Intermedio-Avanzado)

Este paquete contiene 15 experiencias (3 por tópico) para cursos universitarios de robótica móvil, percepción y control.

## Estructura

- [01_movimiento_simple.md](01_movimiento_simple.md)
- [02_camara.md](02_camara.md)
- [03_lidar.md](03_lidar.md)
- [04_seguimiento_linea.md](04_seguimiento_linea.md)
- [05_deteccion_objetos.md](05_deteccion_objetos.md)

## Tópicos cubiertos

1. Movimiento simple del auto
2. Cámara
3. Lidar
4. Seguimiento de línea
5. Detección de objetos

## Formato de cada experiencia

Cada experiencia incluye:
- Contexto semiaplicado (escenario realista)
- Objetivo técnico
- Preparación y comandos base
- Tareas guiadas
- Entregables
- Criterios de evaluación sugeridos

## Comandos base comunes

En terminal 1 (simulación):

```bash
source /opt/ros/humble/setup.bash
cd /root/ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch qcar_gazebo qcar_world.launch.py
```

En terminal 2 (nodos):

```bash
source /opt/ros/humble/setup.bash
cd /root/ros2_ws
source install/setup.bash
```

## Recomendación docente

- Duración sugerida por experiencia: 90 a 120 minutos.
- Tamaño de grupo: 2 a 3 estudiantes.
- Evaluación: ponderar tanto resultados experimentales como calidad de análisis técnico.
