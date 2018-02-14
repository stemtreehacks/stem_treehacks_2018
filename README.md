# About the challenge

We are asking you to forecast one site's energy consumption and simulate activity of an energy storage system in order to reduce this client's energy bill through peak shaving.

## Peak shaving primer

**For a more in depth explanation of peak shaving and other relevant information for this challenge come to our talk on Friday at 10:30PM.**

Larger users of electricity have two parts on their electricity bills:
1. Energy charges ($/kWh)
2. Demand charges ($/kW)

Demand charges are calculated based on the highest 15 minute average usage within a given month. For facilities that use a lot of power over shorter periods of time, this demand charge could comprise a significant portion of their electricity bill. 

Peak shaving with energy storage involves intelligently discharging during these peaks (shaving them so to speak) such that the customer's electricity demand is effectively lowered in the eyes of the utility. This reduces the customer's demand charges.

# About the data

You have been given one year of site load data. There may be missing data that you will have to treat appropriately. 

There is additional system data you are free to use or disregard as you see fit:
* zip code: 12345
* nameplate: 18kW/30kWh
* tariff: $10/kW demand charge applicable all the time
* billing cycles: matches calendar years

# Things you may consider building

* robust data pipeline to handle training and testing data
* machine learning model(s) to forecast load
* simulation of the energy storage system

# How winners will be determined

We will be judging your team's model and algorithm based on your results for team's result for January 2018. 

Submit the following by making a pull request against our repo:
* your team's forecast for January 2018 as a CSV. It should be formatted in the same way as the data we have provided.
* your team's forecasted savings (i.e. original forecasted peak vs. post-storage activity peak) for January 2018 as a comment in your pull request. 

The winning team will be the team with the forecast and savings that are closest the maximum achievable based on the actual load for this month.

# About Stem

Find out more about us at [our website](http://www.stem.com).

## Contact us

For those students who are interested in internship opportunities with us, you can visit [our career page](https://stem.silkroad.com) and enter your contact info [here](https://goo.gl/forms/wqxFNz262CnpMTlj1).