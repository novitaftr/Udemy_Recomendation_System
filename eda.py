import pandas as pd

import plotly.express as px

class DataProcess:

    def __init__(self, path):
        self.path = path 
    
    def load(self):
        df = pd.read_csv(self.path)

        #cleaned the image to be displayed in the web
        df['image'] = df['image'].apply(self.image_cleaned)

        #adding udemy url for which the title can be clicked and be directed to udemy website
        df['course_url'] = df['course_url'].apply(self.udemy_url)

        # renaming display_name to user_name
        df = df.rename(columns={'display_name' : 'user_name'})
        return df

    def unique(self, df):
    
        data = df.drop_duplicates(subset='title').reset_index(drop=True)
        return data[['course_id', 'title', 'category', 'subcategory', 'topic', 'price', 'headline', 
                     'avg_rating', 'num_subscribers', 'course_url', 'instructor_name',  'image']]

    def image_cleaned(self, url):
        return url.replace("img-b", "img-c")

    def udemy_url(self, url):
        return 'https://www.udemy.com' + url
    

class DataExploratory:

    def __init__(self, df):
        self.df = df
    
    def most_popular(self, data, by='num_subscribers', column='category', n=5):

        # Get top courses by categories according to highest num_subscribers
        most_popular_courses = data.sort_values(by=by, ascending=False).groupby(column).head(n)

        most_popular = most_popular_courses[['course_id', 'title', 'category', 'subcategory', 'topic', 'price', 'headline', 
                                            'avg_rating', 'num_subscribers', 'course_url', 'image']]
        most_popular.sort_values(by=by, ascending=False)

        return most_popular

    def feature_count(self, column:str, n=10) -> pd.DataFrame:
        #counting a feature in interest
        counts = self.df.groupby(column).size().reset_index(name='count')
        return counts.sort_values(by='count', ascending=False)[:n]
    
    def feature_plot(self, column:str):
        feature = self.feature_count(column).sort_values(by='count', ascending=True)

        fig = px.bar(feature, y = column, x='count', text_auto=True)

        fig.update_layout(title_text=f'Top {len(feature)} courses by {column.capitalize()}',
                          yaxis_tickfont_size=14, yaxis=dict(title=''),
                          xaxis=dict(title='Count',titlefont_size=16,tickfont_size=14))
        return fig

    def subcategory_plot(self, category:str):

        df_cat = self.df[self.df['category']==category]
        feature = df_cat.groupby('subcategory').size().reset_index(name='count')
        feature = feature.sort_values(by='count', ascending=True)

        fig = px.bar(feature, y = 'subcategory', x = 'count', text_auto=True)

        fig.update_layout(title_text=f'Top courses in Category :  {category.capitalize()}',
                          yaxis_tickfont_size=14, yaxis=dict(title=''),
                          xaxis=dict(title='Count',titlefont_size=16,tickfont_size=14))
        
        return fig

    def instructor_plot(self, n=5):
        instructor_count = self.df.groupby('instructor_name')['num_subscribers'].sum().reset_index()
        top_instructor = instructor_count.sort_values(by='num_subscribers', ascending=False)[:n]

        fig = px.bar(top_instructor, x = 'instructor_name', y = 'num_subscribers', text_auto=True)

        fig.update_layout(title_text=f'Top {n} Performing Instructor based on Total Subscribers',
                          yaxis_tickfont_size=14, yaxis=dict(title=''),
                          xaxis=dict(title='',titlefont_size=16,tickfont_size=14))
        return top_instructor, fig

    def topic_plot(self, n=5):
        topic_subscribers = self.df.groupby('topic')['num_subscribers'].sum().reset_index()
        top_topic_subs = topic_subscribers.sort_values(by='num_subscribers', ascending=False)[:n]

        fig = px.bar(top_topic_subs, x = 'topic', y = 'num_subscribers', text_auto=True)

        fig.update_layout(title_text=f'Top {n} Topic Courses based on Total Subscribers',
                          yaxis_tickfont_size=14, yaxis=dict(title=''),
                          xaxis=dict(title='',titlefont_size=16,tickfont_size=14))
        return fig

      
