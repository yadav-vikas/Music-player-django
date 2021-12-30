import pandas as pd
import numpy as np
import joblib

import Recommenders

from sklearn.model_selection import train_test_split


#Read userid-songid-listen_count triplets
#This step might take time to download data from external sources
triplets_file = 'https://static.turi.com/datasets/millionsong/10000.txt'
songs_metadata_file = 'https://static.turi.com/datasets/millionsong/song_data.csv'

song_df_1 = pd.read_table(triplets_file,header=None)
song_df_1.columns = ['user_id', 'song_id', 'listen_count']

#Read song  metadata
song_df_2 =  pd.read_csv(songs_metadata_file)

#Merge the two dataframes above to create input dataframe for recommender systems
song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")

train_data, test_data = train_test_split(song_df, test_size = 0.20, random_state=0)
# print(train_data.head(5))

pm = Recommenders.popularity_recommender_py() # popularity based model
pm.create(train_data, 'user_id', 'song')

is_model = Recommenders.item_similarity_recommender_py() # personalised/item-similarity based model
is_model.create(train_data, 'user_id', 'song')

def pm_predict(songs):
    return pm.get_similar_items(songs)

def is_model_predict(songs):
    return is_model.get_similar_items(songs)