#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt
import numpy as np

class LidarVisualizer:
    def __init__(self):
        rospy.init_node('lidar_visualizer', anonymous=True)
        
        # Suscribirse al tópico del LIDAR. '/qcar/scan' es común para este robot.
        rospy.Subscriber('/qcar/scan', LaserScan, self.scan_callback)
        
        # Configurar el gráfico de matplotlib
        plt.ion() # Activar modo interactivo
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='polar')
        self.line, = self.ax.plot([], [], 'o', markersize=2) # 'o' para puntos
        
        self.ax.set_theta_zero_location('N') # 0 grados en el frente
        self.ax.set_theta_direction(-1) # Girar en sentido horario
        self.ax.set_title("LIDAR Data")
        self.ax.set_rlabel_position(90)
        self.ax.set_rmax(10) # Rango máximo en metros, ajustable

        rospy.loginfo("Lidar visualizer node started. Subscribed to /qcar/scan")

    def scan_callback(self, scan_msg):
        """
        Esta función se llama cada vez que se recibe un mensaje de LaserScan.
        """
        # Log para confirmar que recibimos datos
        rospy.loginfo_once(f"Receiving LIDAR data with {len(scan_msg.ranges)} points.")

        # Extraer los rangos y ángulos del mensaje
        ranges = np.array(scan_msg.ranges)
        
        # Reemplazar valores infinitos o cero con NaN para que no se grafiquen
        ranges[np.isinf(ranges)] = np.nan
        ranges[ranges == 0] = np.nan
        
        # Crear un array de ángulos correspondiente a cada medición
        angles = np.linspace(scan_msg.angle_min, scan_msg.angle_max, len(ranges))
        
        # Actualizar los datos del gráfico
        self.line.set_data(angles, ranges)
        
        # Ajustar el límite del radio si es necesario (opcional, puede ser fijo)
        # self.ax.set_rmax(np.nanmax(ranges) if not np.all(np.isnan(ranges)) else 10)
        
        # No es necesario llamar a draw/flush aquí, el bucle principal se encarga

    def run(self):
        # Bucle para mantener el script corriendo y actualizar el gráfico
        rate = rospy.Rate(10) # 10 Hz
        while not rospy.is_shutdown():
            try:
                self.fig.canvas.draw_idle()
                self.fig.canvas.flush_events()
                rate.sleep()
            except Exception as e:
                # Manejar el caso en que la ventana se cierra manualmente
                rospy.loginfo(f"Closing visualizer: {e}")
                break

if __name__ == '__main__':
    try:
        visualizer = LidarVisualizer()
        visualizer.run()
    except rospy.ROSInterruptException:
        print("Shutting down lidar visualizer.")
    except Exception as e:
        print(f"An error occurred: {e}")

