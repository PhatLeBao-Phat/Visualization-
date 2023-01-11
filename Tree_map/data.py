import os 
import pandas as pd 
import numpy as np 

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "explore_dataset\listings.pkl")
FEATURES = [
    'host_total_listings_count',
    'host_response_rate',
    'accommodates',
    'bedrooms',
    'review_scores_rating',
    'review_scores_accuracy',
    'review_scores_cleanliness',
    'review_scores_checkin',
    'review_scores_communication',
    'review_scores_location',
    'review_scores_value',
    'reviews_per_month',
]


def get_custom_df(df, lst_feature):
    """filter custom-data on list of features"""
    df_plot = df.copy()[lst_feature]
    
    return df_plot


def test_data(df):
    "generate test sample"
    df_plot = df.dropna(inplace=False)
    df_plot = df_plot.iloc[1:1000, :]
    df_plot = df_plot.reset_index(drop=True)

    return df_plot

# def handle_dtypes(df):
#     """column (68) has unidentified dtype"""
#     col68 = df.columns[68]
#     non_na = df[col68].notna()
#     df[col68][non_na] = df[col68][non_na].copy().astype(str)

#     return df 

df_bnb = pd.read_pickle(PATH)
# df_bnb = handle_dtypes(df_bnb)
df_plot = get_custom_df(df_bnb, FEATURES)
df_plot = test_data(df_plot)
