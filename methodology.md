Methodology
===========

Themes are generated based on a supervised model trained on the New York Times corpus. Each story in that corpus is tagged with a set of "descriptors". The model was fed those descriptors as a training set, using word embeddings as the central training feature. Recall was 0.82, and precision of this model was 0.27; leading to an f1 score of 0.406.

The model used was created by Jasmin Rubinovitz as part of her thesis work at the MIT Media Lab.

### Training

This was trained on the [NYT Annotated Corpus](https://catalog.ldc.upenn.edu/ldc2008t19). During training - 85% of the articles in the corpus were used, and the rest (15%) were reserved as a test set. On that test set both recall and precision were above 0.97.

### Evaluation

Since the corpus include only articles from the years 1987-2007, it was important to validate it on more recent articles as well. For this purpose, we used the NYT API, which allows developers to query the nytimes.com and retrieve articles and their semantic labels. We retrieved a random set of 3,000 articles from the New York Times website, published between 2010 to 2016.

On that set, evaluation results had an average of precision: 0.590366. This score corresponds to the area under the precision- recall curve. For comparison, a study that compared various SVM and LDA algorithms for multi-label classification on news documents presents scores between 0.449 - 0.612, evaluated on the original NYT corpus dataset. 

Label ranking loss: 0.057090. This is the ranking loss which averages over the samples the number of label pairs that are incorrectly ordered, i.e. true labels have a lower score than false labels, weighted by the inverse number of false and true labels. The best achievable ranking loss is zero. The same study mentioned above present scores label ranking loss between 3.51 - 0.93 on the NYT dataset. 

Another evaluation for the same 3000 articles set included the conversion of the resulted labels frequency vector  for each article to a 0-1 vector (every label with probability > 0.01 = 1 and the rest are 0). Results for this evaluation were recall of 0.82 and precision of 0.27 .

### More Technical Details

The model is a convolutional neural network, trained as a multi-label classifier for classifying news stories to different topics (i.e. descriptors and taxonomies from the New York Times annotated corpus). The is built to learn the training corpus to assign labels to arbitrary text and can be used to predict those labels on unknown data. 

### About the NYT Corpus

The NYT annotated corpus is a corpus drawn from the historical archive of the New York Times and it includes metadata provided by the New York Times Newsroom, the New York Times Indexing Service and the online production staff at nytimes.com. This corpus contains nearly every article published in the New York Times between January 01, 1987 and June 19th, 2007. Articles are tagged for persons, places, organizations, titles and topics using a controlled vocabulary that is applied consistently across articles. 
