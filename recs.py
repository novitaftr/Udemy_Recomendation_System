from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd

from surprise import dump

from collections import defaultdict

class ContentBased:
    
    def __init__(self, df):
        self.df = df 
                       
    def compute_similarity(self):

        unique = self.df
        dummies = pd.get_dummies(unique['subcategory']).groupby(level=0).sum()
        similarity = cosine_similarity(dummies)
        return similarity
    
        # Function to get the recommended course
    def recommendations(self, title, top_n=10):

        unique_df = self.df
        similarity = self.compute_similarity()

        # Find the index of the courses with the given title
        idx = unique_df[unique_df['title'] == title].index[0]

        # Get the cosine similarity scores for the courses
        similarity_scores = list(enumerate(similarity[idx]))

        # Sort the similarity scores in descending order
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Get the top_n courses indices
        courses_indices = [i[0] for i in similarity_scores[1:top_n+1]]

        # Return the top_n most similar courses
        return unique_df['title'].iloc[courses_indices].values.tolist()


class CollaborativeFiltering:

    def __init__(self, path, df):
        self.path = path
        self.df = df
    
    def course_data(self, df):
        return df[['course_id', 'title', 'category', 'subcategory', 'topic', 'price', 'headline', 
                   'avg_rating', 'num_subscribers', 'course_url', 'instructor_name',  'image']]
    
    def rating_data(self):
        return self.df[['user_name', 'course_id', 'rate']]
    
    def predict_load(self):

        filename = self.path
        pred, _ = dump.load(filename)

        return pred

    def get_top_n(self, predictions, user_name, course_df, ratings_df, n = 10):

        '''Return the top N (default) of course_id for a user,.i.e. userID and history for comparison
        Args:
        Returns: 
    
        '''
        #Peart I.: Surprise docomuntation
        
        #1. First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, _, est, _ in predictions:
            top_n[uid].append((iid, est))

        #2. Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key = lambda x: x[1], reverse = True)
            top_n[uid] = user_ratings[: n ]
        
        #Part II.: inspired by: https://beckernick.github.io/matrix-factorization-recommender/
        
        #3. Tells how many movies the user has already rated
        user_data = ratings_df[ratings_df.user_name == (user_name)]
        print('User {0} has already rated {1} courses.'.format(user_name, user_data.shape[0]))

        
        #4. Data Frame with predictions. 
        preds_df = pd.DataFrame([(id, pair[0],pair[1]) for id, row in top_n.items() for pair in row],
                                columns=["user_name" ,"course_id","rat_pred"])
        
        
        #5. Return pred_usr, i.e. top N recommended movies with (merged) titles and genres. 
        pred_usr = preds_df[preds_df["user_name"] == (user_name)].merge(course_df, how = 'left', 
                                                                        left_on = 'course_id', right_on = 'course_id')
                
        #6. Return hist_usr, i.e. top N historically rated movies with (merged) titles and genres for holistic evaluation
        hist_usr = ratings_df[ratings_df.user_name == (user_name) ].sort_values("rate", ascending = False).merge\
        (course_df, how = 'left', left_on = 'course_id', right_on = 'course_id')
        
        
        return hist_usr, pred_usr