# IoT-Based-Fire-Predition-System

Our goal was to design a system able to predict fires, in essence, forest fires way before they have a chance to start.

To grasp the state of the elements of the environment that contribute to bringing forth a forest fire and alert whoever will be utilizing our app and thus responsible for tackling the situation.

The device we had in mind was to be small, easily deployable, and capable of cloud connectivity.


For our solution, we used  Pi as a central hub for collecting and processing sensor data to give our outputs, which consists of not only the probability of a fire, but also the sensor data we retrieved in order to keep the app user updated with the environment situation and not just have them look at a value of probability alone.

Our model which is stored and executes on the Raspberry Pi is a machine learning algorithm. We trained and tested it using a fire dataset to make it capable of predicting based on environmental values the chances of a fire.

The data from the model on the Pi is then sent to ThingSpeak, which is an IoT analytics platform we chose. ThingSpeak allows us to store and visualize live data streams of what we’re sending in the cloud.

Then we have our mobile application which serves as a dashboard for the user to see real-time and previous data collected from the Pi.
The user also has the option to choose the probability to set the alarm system to

![image](https://user-images.githubusercontent.com/32312941/113818838-444ab000-972d-11eb-9bc3-d70644d2257a.png)




YouTube video link to the product information https://www.youtube.com/watch?v=NqyOzydDMyw
