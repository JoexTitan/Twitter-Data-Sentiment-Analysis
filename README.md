# Twitter Data Sentiment Analysis

<img src="https://media.springernature.com/lw685/springer-static/image/chp%3A10.1007%2F978-1-4842-7182-7_1/MediaObjects/511918_1_En_1_Fig1_HTML.jpg" width="950" height="300" />


## Introduction

In the following warehousing project we will extract, transform, and load the data from Twitter API, afterwhich we will deliver analysis for reporting purposes. 
For this project you will be required to have the following MS BI tools: SSIS (Integration Services), SSAS (Analysis Services), SSRS (Reporting Services), SSMS (Management Studio), and Microsoft Power BI.


## ETL Pipeline
The first component is located inside `get_twitter_data` Its primary function is to get tweets for our analysis, some sample data is provided for you in `extracted_data_samples`. 

You need to get Twitter credentials via https://developer.twitter.com/en/apps in order to gain access to the authentication tokens, 
afterwhich you will be able to interact with twitter API. 

We will be using `Scrapy 2.7.1` in order to crawl through the the desired records and `google-cloud-language` library to enhance sentiment accuracy throughout the NLP analysis.


<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/SSIS01.jpg" width="900" height="700" />
<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/SSIS02.jpg" width="900" height="670" />
<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/SSIS03.jpg" width="900" height="650" />
<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/SSIS05.jpg" width="900" height="710" />



## SSAS Modeling
Prior to removing Twitter duplicates, we must first convert our data from JSON to CSV and create all necessary sourced attributes. 

The `twitter_batch_prep` scripts will utilize multi-threading to optimize the I/O processes, the results will be saved in a csv file so that you can merge them later on your own.

<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/schema01.jpg" width="900" height="750" />



## Power BI (Reporting)

<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/vis_gif_02.gif"/>
<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/vis_gif_04.gif"/>
<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/vis_gif_03.gif"/>
<img src="https://github.com/JoexTitan/Social-Media-Sentiment-Analysis/blob/master/presentation_visuals/vis_gif_01.gif"/>





