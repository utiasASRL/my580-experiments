ros2 run apriltag_ros apriltag_node --ros-args \
    -r image_rect:=/zed2i/zed_node/left/image_rect_color \
    -r camera_info:=/zed2i/zed_node/left/camera_info \
    -r detections:=detections/left \
    --params-file /home/asrl/research/my580-experiments/workspace/params/tags_left.yaml
