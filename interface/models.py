from json.tool import main
import pickle as pkl
import csv
import pandas as pd
import numpy as np
from filter import Filter

class BaseModel:
    def __init__(self, model_pkl, data_csv='data4_01.csv'):
        self.model = self.load(model_pkl)
        self.df_filters = pd.read_csv(f'../data/{data_csv}')

    def recommend(self, movie_1):
        pass


    def predict(self, x_test):
        return self.model.predict(x_test)

    def load(self, model_pkl):
        return pkl.load(open(model_pkl, 'rb'))


class KNN_COLLAB(BaseModel):
    def __init__(self, model_pkl, data_csv='../data4_01.csv'):  # likely extra inputs wont be needed, but just in case...
        from sklearn.neighbors import NearestNeighbors

        self.utility_matrix = self.load_util()

        # knn = NearestNeighbors(algorithm='brute', metric='cosine')
        self.model = NearestNeighbors(n_neighbors=11)
        self.model.fit(self.utility_matrix.values, )


    def avg_vec(self, movie):
        helper = np.zeros((1,610))
        for mov_id in movie:
            print('retrieved', mov_id)
            helper = np.add(helper, self.utility_matrix.iloc[mov_id].values.reshape(1,-1) )


        return helper/len(movie)


    def smart_vec(self, movie): # better way than averaging?
        pass


    '''
    return a df of movies for filter to deal with
    '''
    def recommend(self, movie, filters):
        feature_input = self.avg_vec(movie)
        distances, indices = self.model.kneighbors(feature_input, n_neighbors = 9710)
        m=pd.Series(indices[0], name='movie')
        d=pd.Series(distances[0], name='distance')

        # distances, indices = knn.kneighbors(utility_matrix.iloc[random_movie].values.reshape(1,-1), n_neighbors = 11)

        recommendations = pd.concat([m,d], axis=1).sort_values(by='distance', ascending=True)
        f = Filter()
        recommendations = f.all_filters(recommendations, movie, filters)
        # return recommendations[:10]

        #change later...
        return [self.utility_matrix.index[x] for x in recommendations]  # df
        
    
    def load_util(self):
        utility_matrix = pd.read_csv('data/user_rating_matrix.csv', index_col=0)
        utility_matrix.columns.name = utility_matrix.index.name
        utility_matrix.index.name = 'title'
        return utility_matrix


# if __name__ == '__main__':
#     knn = KNN_COLLAB('12', '12')
#     movie = 8001
#     filter = 'no filter'
#     knn.recommend(movie, filter)