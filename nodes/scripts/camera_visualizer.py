#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

class CameraVisualizer:
    def __init__(self):
        rospy.init_node('camera_visualizer', anonymous=True)

        while rospy.get_time() == 0:
            rospy.loginfo_once("Waiting for simulation time to be ready...")
            rospy.sleep(0.1)
        
        # El tópico de la cámara puede variar. '/camera/color/image_raw' es común.
        # Hacemos que sea un parámetro para que puedas cambiarlo fácilmente desde el launch file.
        image_topic = rospy.get_param('~image_topic', '/camera/color/image_raw')
        
        self.bridge = CvBridge()
        
        # Suscribirse al tópico de la imagen de la cámara
        self.image_sub = rospy.Subscriber(image_topic, Image, self.image_callback)
        
        self.window_name = "QCar Camera Feed"
        self.cv_image = None
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        
        rospy.loginfo(f"Camera visualizer node started. Subscribed to {image_topic}")
        rospy.loginfo("A window should appear showing the camera feed.")

    def image_callback(self, msg):
        """
        Esta función se llama cada vez que se recibe un mensaje de Image.
        """
        try:
            # Convertir el mensaje de imagen de ROS a una imagen de OpenCV
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error: {e}")
        
        # Mostrar la imagen en una ventana
        cv2.imshow(self.window_name, cv_image)
        
        # Esperar un poco. Es necesario para que la ventana se actualice.
        cv2.waitKey(3)

    def run(self):
        rate = rospy.Rate(30) # 30 Hz, bueno para video
        while not rospy.is_shutdown():
            # Solo mostrar la imagen si ya hemos recibido una
            if self.cv_image is not None:
                cv2.imshow(self.window_name, self.cv_image)
            
            key = cv2.waitKey(1) & 0xFF
            # Si se presiona 'q' o se cierra la ventana (y la ventana existe), salir
            if key == ord('q') or (cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1 and self.cv_image is not None):
                break
            
            rate.sleep()
            
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        visualizer = CameraVisualizer()
        visualizer.run()
    except rospy.ROSInterruptException:
        print("Shutting down camera visualizer.")
    except Exception as e:
        print(f"An error occurred: {e}")
