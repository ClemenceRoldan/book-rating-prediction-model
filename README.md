# Book Rating Prediction Model
Predicting Book Ratings is a university group project developed by Kheirie Kaderi, Clemence Roldan, and Mohamed Al Jalanji for Machine Learning with Python course at Data ScienceTech Insitute. The project aims to predict book ratings using regression models.
## Table of Contents
- [About](#about)
- [Installation](#installation)
- [Notebooks](#notebooks)
- [Utils](#utils)
- [Scraper](#scraper)

## About
This project aims to use machine learning techniques to predict a specific book's rating.

The raw dataset (books.csv) was provided by Data ScienceTech Institute as part of the Python for Machine Learning course given in Autumn 2023. It is a collection of Goodreads books, sourced from real user information. This dataset offers versatility and can be utilized for various tasks, such as predicting book ratings.

Below is the information regarding the dataset features:

- **bookID**: A unique identification number for each book.
- **title**: The name under which the book was published.
- **authors**: The names of the authors of the book. Multiple authors are delimited by “/”.
- **average_rating**: The average rating of the book received in total.
- **isbn**: Another unique number to identify the book, known as the International Standard Book Number.
- **isbn13**: A 13-digit ISBN to identify the book, instead of the standard 11-digit ISBN.
- **language_code**: Indicates the primary language of the book. For instance, “eng” is standard for English.
- **num_pages**: The number of pages the book contains.
- **ratings_count**: The total number of ratings the book received.
- **text_reviews_count**: The total number of written text reviews the book received.
- **publication_date**: The date the book was published.
- **publisher**: The name of the book publisher.

## Installation

To run the project, install the required dependencies using Conda or pip:

```
conda install --file requirements.txt
```
or 

```
pip install -r requirements.txt
```
## Notebooks

The project includes three main notebooks:

- **DataAnalysis.ipynb**: includes analysis of the dataset, exploring its features, and gaining insights into the data. The data used was the df_ml_ds_final1.csv found in the data file. It is the dataset that was resulted from the data cleaning and feature engineering done in the DataCleaningFeatEng.ipynb notebook

- **DataCleaningFeatEng.ipynb**: shows the steps taken towards cleaning the dataset and performing feature engineering to prepare it for regression models. This notebook resulted in the final dataset df_ml_ds_final1.csv datasets found in the data folder, which was used for the data analysis and average ratings prediction

- **Regression.ipynb**: applies and compares basic Linear Regression and Ensemble Tree-Based Regression models to predict book ratings based on the processed dataset.

Further details and explanation are found in the notebooks.

## Utils

The `utils.py` file contains useful functions that were used in data preprocessing and feature engineering.

## Scraper

The Scraper was developed to address various challenges in the dataset, including the presence of multiple editions of the same book and missing information. These issues often resulted in books with identical titles and average ratings, despite being distinct editions or even different books altogether. Additionally, certain books were noted for their unusually low page count, indicative of audio formats rather than traditional printed editions. These complexities necessitated the development of the Scraper to ensure data integrity and accuracy.

The Scraper introduced several additional features to enhance the dataset:

- first_publish : the date a book was first published
- book_format : the format of the book (e.g. paperback, Audio CD, hardcover, ebook)
- new_publisher: the corrected publisher information obtained through scraping, as it was observed that some books had incorrect publishers in the original dataset.
- edition_avgRating: the actaul average rating of each book edition
- added_toShelves: the number of users that added a book to shelves

> **Note:** the Scraper faced limitations in obtaining complete information for the new_publisher attribute. Due to time constraints and the complexity of the scraping process, we relied primarily on the publisher feature available in the original dataset.

Within the Scraper folder, you'll find two essential components:

- **scraper.py**: This Python script houses all the crucial functions utilized for the scraping process.

- **scraper_GoodReads.ipynb**: This Jupyter notebook demonstrates how the scraping process was implemented and applied.

Additionally, `chromedriver.exe` plays a vital role in the scraping process by connecting to the driver to open specific pages.

