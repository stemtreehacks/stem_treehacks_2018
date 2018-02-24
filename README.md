# treehacks-energy challenge
Submission for TreeHacks 2018 - Stem's Challenge.

## [Challenge](https://github.com/stemtreehacks/stem_treehacks_2018)
To forecast one site's energy consumption and simulate the activity of a behind-the-meter energy storage system in order to reduce this client's energy bill through peak shaving.

## Getting Started
The analysis and prediction model (as well as the dataset provided) can be found in this repo. To run, simply modify the path of the file in:
```
analysis.py and seeding_LSTM.py
```
Running the code will yield the results shown below. Alternatively, you can reproduce or enhance the plots:
```
Using: data_points.p
pickle.dump([trainPredict, trainY, testY, testPredict], open(dir+'data_points.p', 'wb'))
```
## Our Solution
Using long term short term memory layer (LTSM),  we are able to learn sequence patterns better by having memory of what it has seen before.

![Learning](https://github.com/yyang0087/treehacks-energy/blob/master/1.png)

As the train decreases over epoch, it's evident that the model is learning.
```
Train Score: 44.57 RMSE
Test Score: 46.17 RMSE
```
Since train and test scores are close, the model can correctly predict on data it hasn't seen yet.

### Main Plot
Here, is comparison of our known data (in blue), our training output (in orange), and our test data (in green).
![Main Plot](https://github.com/yyang0087/treehacks-energy/blob/master/3.png)

One issue that's evident in this plot is that our algorithm consistently underestimates the values. But since the understimation is consistent across time, we can design a correction factor to compensate for the offset.

![Correction Factor](https://github.com/yyang0087/treehacks-energy/blob/master/2.png)
This plot shows what a simple error correction would look like. Notice how the red lines (magnitude of peaks predictions) match the the actual data much more accurately now.

![Zoomed Prediction](https://github.com/yyang0087/treehacks-energy/blob/master/4.png)
It's evident and remarkable when zoomed in that the shape closely matches the actual data. The only issue is the biasing issue, which is why we have a correction factor. This essentially shows the the model can learn qualitative geometric features of the usage by training on past pulses.

### Code source:
- Tensorflow
- Keras

## Acknowledgements
- Built for TreeHacks 2018
- Made by Nathan Zhao, Yu-Lin Yang, and David Ta




# About the challenge

We are asking you to forecast one site's energy consumption and simulate the activity of a behind-the-meter energy storage system in order to reduce this client's energy bill through peak shaving.

## Peak shaving primer

**For a more in depth explanation of peak shaving and other relevant information for this challenge come to our talk on Friday at 10:30PM.**

Large users of electricity have two pieces of their electricity bills:
1. Energy charges ($/kWh)
2. Demand charges ($/kW)

Demand charges are calculated based on the highest 15 minute average usage within a given month. For facilities that use a lot of power over shorter periods of time, this demand charge could comprise a significant portion of their electricity bill. 

Peak shaving with energy storage involves intelligently discharging during these peaks (shaving them so to speak) such that the customer's electricity demand is effectively lowered in the eyes of the utility. This reduces the customer's demand charges.

# About the data

You have been given one year of site load data. There may be missing data that you will have to treat appropriately. 

There is additional system data you are free to use or disregard as you see fit:
* zip code: 92101
* nameplate: 150kW/300kWh
* tariff: $35/kW demand charge applicable over all time
* billing cycles: matches calendar months (i.e. from 1st of month to last)

# Things you may consider building

* robust data pipeline to handle training and testing data
* machine learning model(s) to forecast load
* simulation of the energy storage system

# How winners will be determined

We will be judging your team's model and algorithm based on your results for January 2018. 

Submit the following by making a pull request against our repo:
* your team's forecast for January 2018 as a CSV. It should be formatted in the same way as the data we have provided.
* your team's forecasted savings (i.e. original forecasted peak vs. post-storage activity peak) for January 2018 as a comment in your pull request. 

The winning team will be the team with the forecast and savings that are closest the maximum achievable based on the actual load for this month.

# Job opportunities!

We are looking for interns!

You can visit [our career page](https://stem.silkroad.com) for more information and enter your contact info [here](https://goo.gl/forms/wqxFNz262CnpMTlj1).

## Software Engineering Intern

**Is this your story?**

You are studying Computer Science or a related field at a great school, you like the creative process of developing software and are interested in Machine Learning, Cloud based software or the Internet of Things.

You are ready for an internship at a technology company, but not at any company. You want to spent time with an organization that not only adds value to your education, but one that promotes the use of renewable energy resources and reduces our carbon footprint. 

You may be interested in Stem! We develop the brains to store and use renewable energy. We obviously are passionate about being part of the clean energy wave... but we are not followers... we have created self-learning software that knows when it is the most economical time to store renewable energy and when to release it again. 

We are excited about renewable energy and help reducing the world’s carbon footprint, but at the same time we have created a commercially successful business helping hundreds of organizations, including many Fortune 500 companies. Our customers are great organizations that try to be responsible with their energy usage. And by using Stem, they gain economic benefits at the same time.

We have a great team of software developers; some of us are building a scalable and secure cloud, others enjoy programming IoT devices and make them do magic tricks. We also have a team of data scientists who design machine learning software that lets our service make autonomous decisions about storing, releasing and trading energy. 

Do you have a story that we should hear? Do you feel what we do here at Stem is something that will make you passionate too? If so, we look forward to meeting you and finding out if there is an opportunity for you to intern at Stem!

## About Stem

Stem creates innovative technology services that transforms the way energy is distributed and consumed. Stem’s mission is to build and operate the largest digitally-connected energy storage network for our customers. 

Our world-class analytics will optimize the value of customers' energy assets and facilitate their participation in energy markets, yielding economic and societal benefits while decarbonizing the grid. 

We create automated, price-responsive systems that enable C&I customers to predict and control electricity costs and capture savings in a rapidly-evolving utility landscape. 

The Stem system combines predictive analytics and advanced energy storage with a high-fidelity software user interface. By buffering spikes in energy usage, Stem also reduces the impact of the C&I customer on the utility grid and enables better grid citizenship. Through innovation in technology and financing, our goal is to optimize the relationships between energy providers and consumers.

Find out more about us at [our website](http://www.stem.com).

## What will your internship look like?

This will be a paid internship in our Millbrae or Oakland, CA offices. You will join the Stem software engineering team and be assigned to a Mentor who will guide you while you work on your assigned project. 

You will be joining one of our Scrum teams and learn how to practice the popular Agile Methodology while you work on your project. During your internship, you will have the opportunity to meet with world-class engineers and data scientists and learn how they do their work.

## Who are we looking for:
* Rising undergraduate seniors
* Majoring in CS or related fields

## Job Location:
Millbrae (CA) and Oakland (CA

## Position Type:
Internship – 11/12 weeks
