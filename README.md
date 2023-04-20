# Facial-Recognition-System

This project is a Facial Recognition System that allows user to register and login using their faces on a Django-based webpage. To adddress security and privacy issues, this project develops a liveness face recognition model using machine learning  to prevent from spoofing. An authentication web application that identify and authenticate individuals with their facial data is also established. The account data is protected by an encrypated database on the a MongoDB server and 2-step verification. The web application also provides the permission for users to manage their personal information at any time. This security system can be used for various applications, such as attendance systems.

## Getting Started

### Prerequisites

* Python 3.x
* OpenCV
* face_recognition
* numpy
* Django
* MongoDB

### Installing

1. Clone the repository:
2. Install the required libraries:
   `pip install -r requirements.txt`

### Running the System

1. Run the `manage.py` script:
   `cd prototype`

   `python manage.py runserver`
2. Open a web browser and go to `http://127.0.0.1:8000/facial_auth/` to access the web interface.

### Using the System

The systems consists of 5 main pages: Home page (facial_auth), Signup Page, Login Page, Main Page, and Settings Page.

1. The web starts from the Home page which allows users to Login and Signup.
2. if the user is the first time using this system, they can go to the Signup page to create a new personal account.

   1. At the Signup page, the user enters his/her personal username, email and password fisrt as basic information.
   2. Then users need to start the camera using the Camera Button and capture 5 photos in total of their faces using the Capture Button. 
   It is suggested to take pictures from different angles and light conditions for more compehensive facial features extraction.
   3. Users can submit their information using Signup Button. 
   If there is replicated username or email, or photos are not taken, web will give corresponding repsonse and redirect to Sighup page.
   4. Users can use URLs at the bottom of the webpage to go to Login page or Home page at any time.
![image](https://github.com/yihanchen3/Facial-Recognition-System/blob/yihan/pics/signup.jpeg)
   
3. if the user already has a account created, they can go to the Login page to access the main dashboard.

   1. At the Login page, the user enters his/her own email and password.
   2. If the email and password match, a video will pop up using webcam to do face liveness recognition. 
   Only if the face identification matches the username and the figure is detected as real, the user will be redirected to his Main page.
![image](https://github.com/yihanchen3/Facial-Recognition-System/blob/yihan/pics/login.jpeg)

4. After logging into the system, Main page allows users to go the Settings Page to manage their accounts.

5. At the Setting Page, users can view their attributes containing Name, Email, Password, 2-Step Verification and Delete Account.

   1. Users can update their Name, Email, and Password. 
   If they have set up the 2-Step Verification, they will need to complete a email verification to confirm identity to make modification.
   2. Users can set up a Email Verification by enabling a 2-step verification.
   The 2-step verification allows you to enters a sencondary email and receives a verification code. 
   You can also disable this function after activation.
   3. Users can log out of their accounts and delete all saved private data with one click on the Delete Account.
![image]([https://github.com/lexsaints/powershell/blob/master/IMG/ps2.png](https://github.com/yihanchen3/Facial-Recognition-System/blob/yihan/pics/settings.jpeg))

## Structure of the project

Facial-Recognition-System/
│  README.md
│  requirements.txt
│  
└─prototype
    │  manage.py         
    ├─auth_app
    │  │  admin.py
    │  │  apps.py
    │  │  models.py
    │  │  tests.py
    │  │  urls.py
    │  │  views.py
    │  │  __init__.py 
    │  ├─migrations         
    │  ├─static
    │  │  ├─css
    │  │  │      main.css  
    │  │  └─js
    │  │         video.js        
    │  └─templates
    │         editordel.html
    │         facial_auth.html
    │         login.html
    │         settings.html
    │         signup.html
    │         umain.html
    │         vstep.html
    │         vstep_init.html
    │          
    ├─live_face_detect
    │  │  encode_faces.py
    │  │  face_recognition_liveness_app.py
    │  │  label_encoder.pickle
    │  │  liveness.model
    │  └─face_detector
    │         deploy.prototxt
    │         res10_300x300_ssd_iter_140000.caffemodel
    │          
    └─prototype
          asgi.py
          settings.py
          urls.py
          wsgi.py
          __init__.py



   ## Role of each file


   - `manage.py`: This file is a command-line utility that allows us to interact with the Django project. 
   - `auth_app/`: This folder contains the main Django project files, including the application-specific python files with subdirectories for static, templates, and migrations.
      - `urls.py`: This file maps URLs to views in the application. It contains a list of URL patterns and the view functions to handle each URL. 

      - `views.py`: This file contains the view functions that render the HTML templates. A view function takes an HTTP request as input and returns an HTTP response. It interacts with the models and templates to generate a response that is sent back to the client.

      - `settings.py`: This file contains various configuration settings for the Django application. 

      - `static/`: This folder contains all static files such as CSS, JavaScript, and images. These files are typically used to add style and interactivity to the website.

      - `tempaltes/`: This folder contains the HTML templates for the web app, including the base template and individual pages like the login and upload pages.

   - `live_face_detect/`: This folder contains files for a live face detection application that uses deep learning to identify and verify faces in real-time and check for liveness to prevent spoofing.
      - `encode_faces.py`: This file encodes images captured from the signup webpage and returns the faical data extracted from photos for identification.

      - `face_recognition_liveness_app.py`: This file is the main application file that runs the live face detection and recognition process. It uses the liveness.model file for liveness detection which is a CNN model pre-trained by real and spoofing videos. And it takes label_encoder.pickle and encoded facial data as input and the model from `face_detector/` for face recognition.

- `prototype/`: This folder is the root directory of the Django project, containing the settings and configuration files for the project.
