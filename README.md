# HackIllinois2023
For HackIllinois2023, sw4th1, nzhan2, and Ameat77 created an Automated Trash Classifier.


## What is the problem?

Be sure to write what inspired you, what you learned, how you built your project, and the challenges you faced. Format your story in Markdown.

## What does our project do?



## How did we do this?

### Sources

Kaggle Datasets Used:
Trash: https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification

Fruit: https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition

Electronic: https://www.kaggle.com/datasets/dataclusterlabs/electronics-mouse-keyboard-image-dataset + my own dataset found through google images


### Computer Vision and Cloud Computing

### Natural Language Processing

#### Main Idea:
Utilizing computer vision to analyze a user-inputted image, we generate a predicted name for the object in the image. The specific NLP task we implemented was "named entity recognition", which identifies words or phrases as useful entities. Using this predicted name, we categorized it into the different bins used in the German trash sorting system. First, we imported our necessary packages. For this part of the project, we used import csv, fileinput, autocorrect, webcolors, numpy, math, collections, and nltk. 

#### What is NLTK:
NLTK (Natural Language Toolkit) is a popular platform that works with language data. Utilizing semantic reasoning libraries, we reached a logical conclusion based on predicted name to generate synonyms and hyponyms for a pre-created set of potential trash items under each bin category. We did this in order to create a more expansive and inclusive data set that can accomodate a wider range of potential user images. 

#### Special Cases:
One of our categories was glass, and in Germany, glass is categorized into green, brown, and white. Using webcolors, we converted given glass color into its rgb int values and cross-referenced these values to approximate which out of the three glass categories it would fit best in. Given that some objects could be present under multiple bins, we created an order of priority to properly sort these objects. And some objects, like paper, is a substring of many different trash items that fit into different bins (such as wax paper, toilet paper, paper towels, etc.). To overcome this issue, we prioritized the bin in which the inputted string exactly matched the data element. Furthermore, since some trash items could be contaminated with organic materials, we created a case where any object that was contaminated would automatically be sorted into residual waste. As a fail-safe in case the computer vision couldn't identify the object, we also created a functionality for the user to type their object. To account for misspellings, we also created an autocorrect function to correct user input. 

### Front-End Development (React.js, 3D-Modeling, and Flask)

For our front-end, we created an interative web-app where users can enter pictures of their trash or a description of their trash, and the output will 



## How to recreate our project!

```
git clone https://github.com/Ameat77/HackIllinois2023.git
```
```
pip install -r requirements.txt
```
```
npm start
```
