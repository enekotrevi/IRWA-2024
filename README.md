# IRWA-2024

## Group
**Grup: G_102_8**

## Summary
 Based on the learned from theoretical classes, the seminars, the lab exercises and your own
 research, you are asked to build a search engine implementing different indexing and ranking
 algorithms.
 You are asked to implement four incremental steps that must be delivered on predefined dates:
 <table>
  <thead>
    <tr>
      <th>Part</th>
      <th>Topic</th>
      <th>Delivery Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./part 1">Part 1</a></td>
      <td>Text Processing and Exploratory Data Analysis</td>
      <td>21/10/2024</td>
    </tr>
    <tr>
      <td><a href="./Part 2. Indexing and Evaluation">Part 2</a></td>
      <td>Indexing and Evaluation</td>
      <td>29/10/2024</td>
    </tr>
    <tr>
      <td><a href="./Part 3. Ranking">Part 3</a></td>
      <td>Ranking</td>
      <td>14/11/2024</td>
    </tr>
    <tr>
      <td><a href="#">Part 4</a></td>
      <td>User Interface and Web Analytics</td>
      <td>02/12/2024</td>
    </tr>
  </tbody>
</table>

## Project Instructions
**Part 1: Text Processing and Exploratory Data Analysis**

In this initial part of the project, you will find the first steps we have done.  Between them, the importantion of the different files, that will be used in the project are located in the Data folder. Besides, a pre-processing for the tweets has been permormed using process_tweet() function. 

Next, in the second section, we have analize different studies to a better understand of the data. Some of these studies include: Word cloud, Correlation Matrix, Average,... 

The results of these studies can be observed [here](./part%201/IRWA-2024-u186663-u172936-u186652-part-1.pdf)

Finally, to make use of the notebook, you simply need to run each of the cells in order and you have to put the rute in the corresponding site.

**Part 2: Indexing and Evaluation**

In this scenario, the primary focus is on indexing and evaluation. The data preparation process involves integrating previous work into a new notebook, generating a new dataframe, and indexing tweets to build inverted indexes. For this task, a custom function called "create_index" is developed.

A search engine, named "search," is implemented to retrieve tweets based on specific queries using keywords generated from word cloud analysis. The evaluation is divided into two parts: one focusing on a subset of the dataset and the other using expert judgment to assess the relevance of documents. Various evaluation metrics are presented for different queries, comparing two cases. Additionally, the analysis includes a two-dimensional scatter plot created with the T-SNE algorithm to visualize the relationships between tweets in the dataset. A dense cluster of points suggests similarities among tweets in that region, while the symmetrical distribution around the origin indicates balanced word embeddings.

To **run the notebook correctly**, execute the cells in sequential order to ensure no variables lose their values. Replace doc_path_1 and doc_path_2 with the path to your files for proper loading.

Do not execute the following cells after the first run, as they are only necessary to initialize the data:

1. num_tweets = len(processed_tweets_df)
index, tf, df, idf = create_index_tfidf(processed_tweets_df, num_tweets)

2. def serialize_data(index, tf, df, idf, filepath="index_data.pkl"):
    with open(filepath, 'wb') as f:
        pickle.dump((index, tf, df, idf), f)

3. serialize_data(index, tf, df, idf, filepath=doc_path_1 + "index_data.pkl")

After the first run, with the serialized data saved, you only need to load the data directly. For the last cell, note that the plot is generated very slowly. Instead, you can directly view the saved plot image in the folder for part 2.

**Part 3: Ranking**

In this part, the focus is on ranking documents based on defined queries, specifically finding documents that contain all query terms and sorting them by relevance. The process involves ranking documents using various methods, generating tweet vectors with Word2Vec, and exploring improved representation models like Doc2Vec and Sentence2Vec.

The data preparation process involves integrating previous work into a new notebook, utilizing a dataset containing processed tweets, as well as data from the TF-IDF index, including TF, DF, and IDF values. All required data must be imported through functions defined in the notebook.

To **run the notebook correctly**, execute the cells in sequential order to ensure no variables lose their values. Additionally, replace doc_path_1 and doc_path_2 with the correct file paths to ensure proper data loading. The data used in this part can be found in the "Part 2: Index and Evaluation/Data" section of our GitHub repository to avoid duplication.

**Part 4: User Interface and Web Analytics**

In this final part, our project delivers an intuitive search engine interface with refined result displays, including user-friendly features like a navigation bar, session insights, analysis,... We optimize performance by persistently storing the index for faster loads. On the analytics front, we offer dynamic showcases of user interactions, an intuitive dashboards for document clicks, session analysis, and insightful visualizations of searched queries. Session details, including IP and engagement duration, are captured and saved, enriching user experience. These implementations collectively prioritize user-centric interaction and provide robust analytics for understanding user behavior within the search engine.

For the proper execution of the project, when you want to make a new query, use the button located between the Pompeu Fabra logo and the text 'IRWA Search Engine'. This way, you will be able to correctly save the dwell time of the current query. On the other hand, for the proper handling of documents, when you are on a specific document detail and want to visit a new one, use the 'go back' button. This way, you will correctly save the dwell time of the document you are visiting.

To **run the notebook correctly**, you have to download the zip uploaded in the release of the part 4, where it is the file named 'farmers-protest-tweets.json' because wee have not been able to upload it to the git code because it exceeds the allowed size.
Detailed information about this section and the final results is accessible [here](https://github.com/enekotrevi/IRWA-2024/blob/main/Part%204.%20User%20Interface%20and%20Web%20Analytics/IRWA-2024-u186663-u186652-u172936-part-4.pdf)
