you can add your object detection model here
1- function name must be same
2- in sender.py --> just import inside:

if ALGORITHM =='face':
    from model.face.object_detection import get_object_position 
elif ALGORITHM =='eyes':
    from model.eyes.object_detection  import get_object_position 