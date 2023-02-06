import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge  

import cv2
import apriltag
import numpy as np

class AprilTagRecog(Node):

    def __init__(self, pub_topic, sub_topic):
        # Init node
        super().__init__('AprilTagRecog')
        # Define subscription
        self.sub = self.create_subscription(Image,sub_topic,self.image_callback,10)
        self.subscription  # prevent unused variable warning
        # Define publications
        self.pub_img = self.create_publisher(Image, pub_topic, 10)
        self.pub_tagData = self.create_publisher()

    def image_callback(self, img_msg):
        self.get_logger().info('[AprlTag] New Image:')
        self.get_logger().info(img_msg.header)
        # Bridge from ros to opencv
        bridge = CvBridge()
        image = bridge(img_msg, desired_encoding='passthrough')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Create Detector
        self.get_logger().info("[AprlTag] detecting AprilTags...")
        options = apriltag.DetectorOptions(families="tagcustom48h12")
        detector = apriltag.Detector(options)
        results = detector.detect(gray)
        self.get_logger().info(f"[AprlTag] {len(results)} total AprilTags detected")
        # Process Apriltags and output data.
        # loop over the AprilTag detection results
        for r in results:
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = r.corners
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))
            # draw the bounding box of the AprilTag detection
            cv2.line(image, ptA, ptB, (0, 255, 0), 2)
            cv2.line(image, ptB, ptC, (0, 255, 0), 2)
            cv2.line(image, ptC, ptD, (0, 255, 0), 2)
            cv2.line(image, ptD, ptA, (0, 255, 0), 2)
            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(r.center[0]), int(r.center[1]))
            cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
            # draw the tag family on the image
            tagFamily = r.tag_family.decode("utf-8")
            cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            self.get_logger().info(f"[AprlTag] tag family: {tagFamily}")
            
        # Publish the new image
        img_msg_out = bridge.cv2_to_imgmsg(image, encoding="passthrough")
        self.pub_img.publish(img_msg_out)
        # Publish the 
        pass

# Define main block
def main(args=None):
    rclpy.init(args=args)

    # Spin up left image detector
    pub_topic = 'apriltag/image/left'
    sub_topic = '/zed2/zed_node/left/image_rect_color'
    tag_left = AprilTagRecog(pub_topic,sub_topic)
    rclpy.spin(tag_left)

    rclpy.shutdown()


if __name__ == '__main__':
    main()