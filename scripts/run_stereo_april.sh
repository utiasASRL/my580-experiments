ros2 run apriltag_ros apriltag_node --ros-args \
    -r image_rect:=/zed2/zed_node/left/image_rect_color \
    -r camera_info:=/zed2/zed_node/left/camera_info \
    --params-file params/tags_Custom48h12.yaml