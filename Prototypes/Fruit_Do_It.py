import cv2 as cv

def ScaleImage(input_image, scale_val):
    width = int(input_image.shape[1] * scale_val)
    height = int(input_image.shape[0] * scale_val)

    dim = (width, height)
    result = cv.resize(input_image, dim, interpolation = cv.INTER_AREA)

    return result

def main():
    image = cv.imread("/home/el_zlociako/WDPO_Project/data/05.jpg", cv.IMREAD_COLOR)

    orange_counter = 0
    banana_counter = 0
    apple_counter = 0
    
    with open('dnn_model/coco.names', 'r') as file:
        classes = file.read().splitlines()
    
    net = cv.dnn.readNetFromDarknet('dnn_model/yolov4.cfg', 'dnn_model/yolov4.weights')
    
    model = cv.dnn_DetectionModel(net)
    model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
    
    classIds, scores, boxes = model.detect(image, confThreshold=0.5, nmsThreshold=0.5)
    
    for (classId, score, box) in zip(classIds.squeeze(), scores, boxes):
        fruit_name = classes[classId]

        if fruit_name == "orange":
            cv.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                    color=(0,165,255), thickness=5)
            cv.putText(image, fruit_name, (box[0], box[1]+box[3]-20), cv.FONT_HERSHEY_SIMPLEX, 2,
                    color=(0, 0, 0), thickness=5)
            orange_counter = orange_counter + 1
        
        if fruit_name == "apple":
            cv.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                    color=(0,0,255), thickness=5)
            cv.putText(image, fruit_name, (box[0], box[1]+box[3]-20), cv.FONT_HERSHEY_SIMPLEX, 2,
                    color=(0, 0, 0), thickness=5)
            apple_counter = apple_counter + 1

        if fruit_name == "banana":
            cv.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                    color=(0,255,255), thickness=5)
            cv.putText(image, fruit_name, (box[0], box[1]+box[3]-20), cv.FONT_HERSHEY_SIMPLEX, 2,
                    color=(0, 0, 0), thickness=5)
            banana_counter = banana_counter + 1

    out_image = ScaleImage(image, 0.3)
    
    banana_str = str(banana_counter)
    apple_str = str(apple_counter)
    orange_str = str(orange_counter)
    
    cv.putText(out_image, ("Bananas: " + banana_str), (out_image.shape[1]-100, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                    color=(0, 0, 0), thickness=1)
    cv.putText(out_image, ("Apples: " + apple_str ), (out_image.shape[1]-100, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                    color=(0, 0, 0), thickness=1)
    cv.putText(out_image, ("Oranges: " + orange_str ), (out_image.shape[1]-100, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                    color=(0, 0, 0), thickness=1)

    cv.imshow('Fruits Recognison', out_image)

    while True:
        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()  
