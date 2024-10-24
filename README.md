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
      <td><a href="#">Part 2</a></td>
      <td>Indexing and Evaluation</td>
      <td>29/10/2024</td>
    </tr>
    <tr>
      <td><a href="#">Part 3</a></td>
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
**Part 1:**

In this initial part of the project, you will find the first steps we have done.  Between them, the importantion of the different files, that will be used in the project are located in the Data folder. Besides, a pre-processing for the tweets has been permormed using process_tweet() function. 

Next, in the second section, we have analize different studies to a better understand of the data. Some of these studies include: Word cloud, Correlation Matrix, Average,... 

The results of these studies can be observed [here](./part%201/IRWA-2024-u186663-u172936-u186652-part-1.pdf)

Finally, to make use of the notebook, you simply need to run each of the cells in order and you have to put the rute in the corresponding site.

**Part 2:**

In this scenario, the primary focus is on indexing and evaluation. The data preparation process involves integrating previous work into a new notebook, generating a new dataframe, and indexing tweets to build inverted indexes. For this task, a custom function called "create_index" is developed.

A search engine, named "search," is implemented to retrieve tweets based on specific queries using keywords generated from word cloud analysis. The evaluation is divided into two parts: one focusing on a subset of the dataset and the other using expert judgment to assess the relevance of documents. Various evaluation metrics are presented for different queries, comparing two cases. Additionally, the analysis includes a two-dimensional scatter plot created with the T-SNE algorithm to visualize the relationships between tweets in the dataset. A dense cluster of points suggests similarities among tweets in that region, while the symmetrical distribution around the origin indicates balanced word embeddings.

The results of these studies can be observed here[falta poner el tag].

