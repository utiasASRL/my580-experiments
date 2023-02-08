import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge  
from std_msgs.msg import String
import cv2
import apriltag
import numpy as np
from copy import deepcopy

class AprilTagDetect(Node):

    def __init__(self,topicList):
        # Init node
        super().__init__('apriltag_detect')
        # Define pub and sub dictionaries, keys are sub topic names
        self.sub={}
        self.pub_img={}
        self.pub_info={}
        i = 0
        for topics in topicList:
            # Extract
            sub_topic, pub_topic_img = topics
            # Define publications
            pub_img = self.create_publisher(Image, pub_topic_img, 10)
            # pub_tags = self.create_publisher(..., pub)
            # Define wrapper function to allow new variable input.
            # Local scoping of pubs to fix variables for lambda definition.
            wrapper_fcn = lambda msg, pub_img=pub_img : self.image_callback(msg, pub_img)
            # Define subscription
            self.create_subscription(Image,sub_topic, wrapper_fcn,10)
        # Define apriltag type
        # self.tagtype = "tagCustom48h12"
        self.tagtype = "tag36h11"
       
    
    def image_callback(self, img_msg, pub_img):
        """This function takes in a ros image message and finds the apriltags in the image.
        Apriltag info and new image with bounding boxes are then published to ros.

        Args:
            img_msg (Image): ROS image
        """
        self.get_logger().info('[AprlTag] New Image')
        # self.get_logger().info(img_msg.header)
        # Bridge from ros to opencv
        bridge = CvBridge()
        image = bridge.imgmsg_to_cv2(img_msg, desired_encoding='passthrough')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Create Detector
        self.get_logger().info("[AprlTag] detecting AprilTags...")
        options = apriltag.DetectorOptions(families=self.tagtype)
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
            tagID = str(r.tag_id)
            tagLabel = tagID + ' : '+tagFamily
            cv2.putText(image, tagLabel, (ptA[0], ptA[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            self.get_logger().info(f"[AprlTag] tag family: {tagFamily}")
            
        # Publish the new image
        img_msg_out = bridge.cv2_to_imgmsg(image, encoding="passthrough")
        pub_img.publish(img_msg_out)
        #  TODO : Publish the tag information 

# Define main block
def main(args=None):
    rclpy.init(args=args)

    # define input and output topics
    topicList = [('zed2/zed_node/left/image_rect_color','apriltag/image/left')]
    topicList += [('zed2/zed_node/right/image_rect_color','apriltag/image/right')]
    # Create node and spin up
    tag_detect = AprilTagDetect(topicList)
    rclpy.spin(tag_detect)
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()