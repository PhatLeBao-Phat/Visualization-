import os 
import pandas as pd 
import numpy as np 

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "listings.pkl")
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
    'num_count',
    'room_type',
    'host_is_superhost_cleansed', 
    'neighbourhood_group_cleansed',
    'all',
    'price_cleansed',
    'host_response_rate_cleansed',
    'host_acceptance_rate_cleansed',
    "latitude",
    "longitude",
]


def get_custom_df(df, lst_feature):
    """filter custom-data on list of features"""
    df_plot = df.copy()[lst_feature]
    
    return df_plot


def test_data(df):
    """generate test sample"""
    df_plot = df.dropna(inplace=False)
    df_plot = df_plot.iloc[1:1000, :]
    df_plot = df_plot.reset_index(drop=True)

    return df_plot


def clean_host_is_superhost_cleansed(df):
    """clean host_is_superhost. turn t -> is superhost, turn f to not superhost"""
    df_copy = df.copy()
    df_copy = df_copy.reset_index(drop=True)
    def dcm(row):
        if row == 't':
            return 'is superhost' 
        else:
            return 'not superhost' 
    df_copy['host_is_superhost_cleansed'] = df.host_is_superhost.apply(lambda row: dcm(row)) 
    
    return df_copy


def tree_map_preprocessing(df):
    """preprocessing data for the treemap. Create counting attribute. Dropna for plotting attributes"""
    df_copy = df.copy()
    df_copy.dropna(subset=['room_type','host_is_superhost', 'neighbourhood_group_cleansed'], inplace=True)
    df_copy.reset_index(inplace=True, drop=True)
    df_copy['num_count'] = pd.Series(np.repeat(1, len(df_copy))) # Add a attribute for counting
    df_copy['all'] = 'all' # add root node 

    return df_copy


def handle_dtypes(df):
    """column (68) has unidentified dtype"""
    df_copy = df
    col68 = df_copy.columns[68]
    non_na = df_copy[col68].notna()
    df_copy[col68][non_na] = df_copy[col68][non_na].copy().astype(str)

    return df_copy 

def host_acceptance_rate_clean(df):
    """clean host_acceptance_rate"""
    df_copy = df.copy()
    df_copy.dropna(subset=['host_acceptance_rate'], inplace=True)
    df_copy.reset_index(inplace=True, drop=True)
    df_copy['host_acceptance_rate_cleansed'] = df_copy.host_acceptance_rate.apply(lambda row: float(row.replace('%', '')))

    return df_copy


def host_response_rate_clean(df):
    df_copy = df.copy()
    df_copy.dropna(subset=['host_response_rate'], inplace=True)
    df_copy.reset_index(inplace=True, drop=True)
    df_copy['host_response_rate_cleansed'] = df_copy.host_response_rate.apply(lambda row: float(row.replace('%', '')))

    return df_copy

def price_clean(df):
    df_copy = df.copy()
    df_copy = df_copy[df_copy["price_cleansed"] <= 2000]

    return df_copy

# df_bnb = get_custom_df(df_bnb, FEATURES)
# df_bnb = test_data(df_bnb)
df_bnb = pd.read_pickle(PATH)
df_bnb = clean_host_is_superhost_cleansed(df_bnb)
df_bnb = tree_map_preprocessing(df_bnb)
df_bnb = host_response_rate_clean(df_bnb)
df_bnb = host_acceptance_rate_clean(df_bnb)
df_bnb = price_clean(df_bnb)
df_bnb = get_custom_df(df_bnb, FEATURES)

