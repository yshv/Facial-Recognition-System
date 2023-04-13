#!/bin/bash

# This script is used to run the project in the docker container

RECOGNITION = TRUE
ADD_DATASET = TRUE

if recognition; then

    # FUNCTION_PATH = "face_recognition_and_liveness"
    cd face_recognition_and_liveness
    cd face_recognition

    # Run the face recognition
    python python encode_faces.py -i dataset -e encoded_faces.pickle -d cnn

    # Run the liveness detection
    python recognize_faces.py -e encoded_faces.pickle -d cnn


    python collect_dataset.py -i videos/fake_1.mp4 -o dataset/fake -d face_detector -c 0.5 -s 15
    python collect_dataset.py -i videos/real_1.mp4 -o dataset/real -d face_detector -c 0.5 -s 15

    # additional dataset for training
    if ADD_DATASET; then
        python face_from_image.py -i images/fakes/2.jpg -o dataset/fake -d face_detector -c 0.5
        python face_from_image.py -i images/reals/1.jpg -o dataset/real -d face_detector -c 0.5
    fi


    if [ $? -eq 0 ]; then
        echo "Successfully collected dataset"
    else
        echo "Failed to collect dataset"
    fi

     # Train the model
    python train_model.py -d dataset -m liveness.model -l label_encoder.pickle -p plot.png

    # Test the model
    python liveness_app.py -m liveness.model -l label_encoder.pickle -d face_detector -c 0.5

    if [ $? -eq 0 ]; then
        echo "Successfully trained model"
    else
        echo "Failed to train model"
    fi

fi

python face_recognition_liveness_app.py -m liveness.model -l label_encoder.pickle -d face_detector -c 0.5 -e ../face_recognition/encoded_faces.pickle



