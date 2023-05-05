ros2 run apriltag_ros apriltag_node --ros-args \
    -r image_rect:=/zed2/zed_node/right/image_rect_color \
    -r camera_info:=/zed2/zed_node/right/camera_info \
    -r detections:=detections/right \
    --params-file /home/ros/my580_ros2_ws/workspace/params/tags_custom48h12_right.yaml
