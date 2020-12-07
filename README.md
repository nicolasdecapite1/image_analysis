Duplicate Image Detection 
===
Author: Nick DeCapite

### Algorithm
As apart of my work with the Duke Smart Toilet, my role is to perfrom machine learning analysis on stool images for different criterias of detection. 
However, the first step of this process is to obtain the data to perform such analysis.
I created a web crawler that will go through websites and extract downloadable stool image URLs into a CSV file. 
In order to ensure there are no duplicate images, I wrote a detection algorithm that compares the specific hashes of each pixel in every image. It then compares the 
hashes of each image and calculates a similiarity statistic. If it is under a threshold of 0.05, they are considered duplicate and are deleted from my local folder 
where they are stored.
