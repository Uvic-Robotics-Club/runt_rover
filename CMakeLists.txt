cmake_minimum_required(VERSION 2.8.3)
project(runt_rover)

find_package(catkin REQUIRED COMPONENTS
    std_msgs
    geometry_msgs
    rospy
)


include_directories(${catkin_INCLUDE_DIRS})
generate_messages(DEPENDENCIES std_msgs geometry_msgs)
catkin_package()
