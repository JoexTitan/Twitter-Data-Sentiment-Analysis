# Twitter Data Sentiment Analysis





## Introduction

In the following warehousing project we will extract, transform, and load the data from Twitter API, afterwhich we will deliver analysis for reporting purposes. 
For this project you will be required to have the following MS BI tools: SSIS (Integration Services), SSAS (Analysis Services), SSRS (Reporting Services), SSMS (Management Studio), and Microsoft Power BI.


## ETL Pipeline
The first component is located inside `get_twitter_data` Its primary function is to get tweets for our analysis, some sample data is provided for you in `extracted_data_samples`. 

You need to get Twitter credentials via https://developer.twitter.com/en/apps in order to gain access to the authentication tokens, 
afterwhich you will be able to interact with twitter API. 

We will be using `Scrapy 2.7.1` in order to crawl through the the desired records and `google-cloud-language` library to enhance sentiment accuracy throughout the NLP analysis.








## SSAS Modeling
Prior to removing Twitter duplicates, we must first convert our data from JSON to CSV and create all necessary sourced attributes. 

The `twitter_batch_prep` scripts will utilize multi-threading to optimize the I/O processes, the results will be saved in a csv file so that you can merge them later on your own.









## Power BI (Reporting)







