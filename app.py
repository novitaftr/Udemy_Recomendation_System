import streamlit as st

from recs import ContentBased, CollaborativeFiltering
from eda import DataProcess, DataExploratory

import hydralit_components as hc

# set layout wide
st.set_page_config(page_title='Udemy Recommendation System', layout="wide", page_icon=":computer:")

menu_data = [
        {'icon': "fas fa-tachometer-alt", 'label':"Dashboard", 'ttip':"Interactive Dashboard"},
        {'icon': "far fa-chart-bar", 'label':"Recommendation", 'ttip':"Course Recommendation and Prediction"},
        {'icon': "bi bi-hand-thumbs-up", 'label':"Summary", 'ttip':"Summary and Notes"},
        {'icon': "far fa-address-book", 'label':"Contact Me", 'ttip':"Contact Me"},
]

over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#87CEFA','txc_active':'black','option_active':'white'}
menu_id = hc.nav_bar(menu_definition=menu_data, home_name='Home', override_theme=over_theme)

with st.sidebar:
    st.title('Udemy Course App')
    st.write('Made using **streamlit** by **Novita Fitriani**')

path = 'data/udemy_sample_30.csv'

dp = DataProcess(path)
df = dp.load()
df_unique = dp.unique(df)

eda = DataExploratory(df)

if menu_id == 'Home':

    st.title('Udemy Course Recommendation System')
    st.divider()

    st.image('img/background.png', width=720, use_column_width='always')

    st.divider()
    st.subheader('Top Courses by Topic')

    topic = df['topic'].unique()

    index = list(topic).index('Deep Learning')

    choose = st.selectbox('Pick the topic that interest you', options=topic, index=index)

    topic_popular = eda.most_popular(data=df_unique, by='num_subscribers', column='topic')
    topic_popular = topic_popular[topic_popular['topic'] == choose].reset_index(drop=True)
    
    with st.container():

        st.subheader(f'Top 5 Most Popular Courses by Topic of : {choose}')

        cols = st.columns(topic_popular.shape[0])

        for i in range(len(cols)):

            cols[i].write(f"[{topic_popular['title'][i]}](%s)" % topic_popular['course_url'][i] )
            cols[i].image(topic_popular['image'][i], 
                        caption='{} | {}'.format(topic_popular['category'][i],
                                                topic_popular['subcategory'][i]))
            caps = f"""
            *{topic_popular['headline'][i]}* \n
            **Price** : $ {topic_popular['price'][i]}\n
            **Rating** : {round(topic_popular['avg_rating'][i],2)} :star: \n 
            **Total Subscribers** : {topic_popular['num_subscribers'][i]:,} learners
            """
            cols[i].caption(caps)

    st.divider()

    st.subheader('Top Courses by Category')

    category = df['category'].unique()

    choose_cat = st.selectbox('Pick the topic that interest you', options=category)

    category_popular = eda.most_popular(data=df_unique, by='num_subscribers', column='category', n=5)
    category_popular = category_popular[category_popular['category'] == choose_cat].reset_index(drop=True)
    
    with st.container():

        st.subheader(f'Top 5 Most Popular Courses by Category : {choose_cat}')

        cols = st.columns(category_popular.shape[0])

        for i in range(len(cols)):
            cols[i].write(f"[{category_popular['title'][i]}](%s)" % category_popular['course_url'][i] )
            cols[i].image(category_popular['image'][i], 
                        caption='{} | {}'.format(category_popular['category'][i],
                                                category_popular['subcategory'][i]))
            caps = f"""
            *{category_popular['headline'][i]}* \n
            **Price** : $ {category_popular['price'][i]}\n
            **Rating** : {round(category_popular['avg_rating'][i],2)} :star: \n 
            **Total Subscribers** : {category_popular['num_subscribers'][i]:,} learners
            """
            cols[i].caption(caps)

    st.divider()

if menu_id == 'Dashboard':

    st.title('Udemy Course Dashboard :computer:')
    st.divider()

    st.subheader('Best Udemy Courses by Category and Subcategory')

    features = ['category', 'subcategory']

    cols = st.columns(2)
    for i in range(len(cols)):
        fig = eda.feature_plot(features[i])
        cols[i].plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader('Top Courses in each Category')

    cat_unique = df['category'].unique()

    choose = st.selectbox('Select category you want to visualize!', options=cat_unique)
    subcat = eda.subcategory_plot(choose)
    st.plotly_chart(subcat, use_container_width=True)

    st.divider()

    cols = st.columns(2)

    instructor, instructor_plot = eda.instructor_plot()
    
    cols[0].subheader('Top Performing Instructor')
    cols[0].plotly_chart(instructor_plot, use_container_width=True)

    topic = eda.topic_plot()

    cols[1].subheader('Top Topic Courses')
    cols[1].plotly_chart(topic, use_container_width=True)

    st.info('Check what each top instructor teach on Udemy course')
    select_instruc = st.selectbox('Select the instructor you want to see', options=instructor)

    df_instructor = df_unique[df_unique['instructor_name'] == select_instruc]
    df_instructor = df_instructor.sort_values(by='num_subscribers', ascending=False).reset_index(drop=True)[:5]

    with st.container():

        st.subheader(f'Top 5 Most Popular Courses by Instructor : {select_instruc}')

        cols = st.columns(df_instructor.shape[0])

        for i in range(len(cols)):
            cols[i].write(f"[{df_instructor['title'][i]}](%s)" % df_instructor['course_url'][i] )
            cols[i].image(df_instructor['image'][i], 
                        caption='{} | {}'.format(df_instructor['category'][i],
                                                df_instructor['subcategory'][i]))
            caps = f"""
            *{df_instructor['headline'][i]}* \n
            **Price** : $ {df_instructor['price'][i]}\n
            **Rating** : {round(df_instructor['avg_rating'][i],2)} :star: \n 
            **Total Subscribers** : {df_instructor['num_subscribers'][i]:,} learners
            """
            cols[i].caption(caps)

    st.divider()

if menu_id == 'Recommendation':
    
    st.title('Recommendation Engine')

    st.divider()

    choose = st.radio('Select whether you are a new user or existing user',
                      options=['New User', 'Existing User'], index=None)
    
    df_index = df_unique.set_index('course_id')
    id_mapping = dict(zip(df_unique['title'], df_unique['course_id']))
    cb_recs = ContentBased(df_unique)

    if choose == None:
        st.warning('Please select those two options: a new user or existing user')

    if choose == 'New User':
        
        title = st.selectbox('Pick Udemy course you want to watch!', 
                                options=df_unique['title'].values, 
                                index=None,
                                placeholder="Select Your Preference's Course ...")
        
        if title == None:
            st.warning("Please select the course you're interested in, and our system will provide the best recommendation for you.")

        else:

            title_id = id_mapping[title]

            with st.spinner('The model is calculated. Please wait ...'):

                st.image(df_index['image'][title_id], caption='{} | {}'.format(df_index['category'][title_id],
                                                                               df_index['topic'][title_id]))
                st.write(f'**Course Link** : [{title}](%s)' % df_index['course_url'][title_id])
                caps = f"""
                        *{df_index['headline'][title_id]}* \n
                        **Price** : $ {df_index['price'][title_id]}\n
                        **Rating** : {round(df_index['avg_rating'][title_id],2)} :star: \n 
                        **Total Subscribers** : {df_index['num_subscribers'][title_id]:,} learners
                        """
                st.caption(caps)

                st.divider()
                st.info(f'Since you pick course about {title}, here are top 10 recommendation courses for you!')

                top_n = cb_recs.recommendations(title)

                id_list = [id_mapping[title] for title in top_n]

                cols = st.columns(5)

                for i in range(len(cols)):

                    cols[i].write(f'[{top_n[i]}](%s)' % df_index['course_url'][id_list[i]])
                    cols[i].image(df_index['image'][id_list[i]], caption='{} | {}'.format(df_index['category'][id_list[i]],
                                                                                          df_index['topic'][id_list[i]]))
                    
                    caps = f"""
                            *{df_index['headline'][id_list[i]]}* \n
                            **Price** : $ {df_index['price'][id_list[i]]}\n
                            **Rating** : {round(df_index['avg_rating'][id_list[i]],2)} :star: \n 
                            **Total Subscribers** : {df_index['num_subscribers'][id_list[i]]:,} learners
                            """
                    cols[i].caption(caps)

                st.divider()

                cols = st.columns(5)

                for i in range(len(cols)):

                    cols[i].write(f'[{top_n[len(cols) + i]}](%s)' % df_index['course_url'][id_list[len(cols) + i]])
                    cols[i].image(df_index['image'][id_list[len(cols) + i]], 
                                caption='{} | {}'.format(df_index['category'][id_list[len(cols) + i]],
                                                        df_index['subcategory'][id_list[len(cols) + i]]))
                    
                    caps = f"""
                            *{df_index['headline'][id_list[len(cols) + i]]}* \n
                            **Price** : $ {df_index['price'][id_list[len(cols) + i]]}\n
                            **Rating** : {round(df_index['avg_rating'][id_list[len(cols) + i]],2)} :star: \n 
                            **Total Subscribers** : {df_index['num_subscribers'][id_list[len(cols) + i]]:,} learners
                            """
                    cols[i].caption(caps)
            
                st.divider()

    if choose == 'Existing User':

        path_predict = 'predictions/knn_collaborative_filtering'
        cf_recs = CollaborativeFiltering(path_predict, df)
        predictions = cf_recs.predict_load()

        users = df['user_name'].unique().tolist()
        user_pick = st.selectbox('Pick the user and you will see their history watching and the recommendation',
                                 options=users, index=None, placeholder='Select the user')
        if user_pick == None:
            st.warning('You have to pick the user first')

        else:

            course_data = df_unique
            rating_data = cf_recs.rating_data()

            hist, pred = cf_recs.get_top_n(predictions, user_pick, course_data, rating_data)
            
            st.info(f'User {user_pick} has already rated {hist.shape[0]} courses')
            
            st.subheader(f"A Snapshot of {user_pick}'s History Watching")

            if hist.shape[0] < 5:
                length = hist.shape[0]
            else:
                length = 5
                
            cols = st.columns(length)
            
            hist = hist.head(5)
            pred = pred.head(5)

            for i in range(len(cols)):

                cols[i].write(f"[{hist['title'][i]}](%s)" % hist['course_url'][i] )
                cols[i].image(hist['image'][i], 
                              caption='{} | {}'.format(hist['category'][i],
                                                       hist['subcategory'][i]))
                caps = f"""
                *{hist['headline'][i]}* \n
                **Price** : $ {hist['price'][i]}\n
                **Rating** : {round(hist['avg_rating'][i],2)} :star: \n 
                **Total Subscribers** : {hist['num_subscribers'][i]:,} learners
                """
                cols[i].caption(caps)


            st.divider()
            st.subheader(f'Course Recommendation for {user_pick}')

            if pred.shape[0] < 5 and pred.shape[0] > 0:
                length = pred.shape[0]
            else:
                length = 5

            cols = st.columns(length)
            
            if pred.shape[0] == 0:
                st.warning(f"Ooppss.. I'm sorry, since you only rated {hist.shape[0]} course, you still don't get the recommendation from our engine. Please pick you as a **New User**")
            else:
                for i in range(len(cols)):

                    cols[i].write(f"[{pred['title'][i]}](%s)" % pred['course_url'][i] )
                    cols[i].image(pred['image'][i], 
                                caption='{} | {}'.format(pred['category'][i],
                                                        pred['subcategory'][i]))
                    caps = f"""
                    *{pred['headline'][i]}* \n
                    **Price** : $ {pred['price'][i]}\n
                    **Rating** : {round(pred['avg_rating'][i],2)} :star: \n 
                    **Total Subscribers** : {pred['num_subscribers'][i]:,} learners
                    """
                    cols[i].caption(caps)

            st.divider()

if menu_id == 'Summary':

    st.title('Summary')
    st.divider()

    st.header('About this Project')

    about = """
    One of the problem faced in every company is they need to retain the customer, not only the user purchase 1 product, but also more.
    So the company's revenue will up, and the business goes on. Recommendation system is a great feature to help answer this issues. 
    Building personalized recommendation which exactly match up with user's preferences can potentially increase the company's retention rate. 
    Allowing some users to not only purchased what they search in the first place, but also get recommendation to other product that complement their needs.

    In this project, the author uses Udemy Course dataset to build personalized recommendation. The dataset can be downloaded from this kaggle links
    [1](https://www.kaggle.com/datasets/hossaingh/udemy-courses) and [2](https://www.kaggle.com/datasets/ankushbisht005/udemy-courses-data-2023).
    
    There are three methods that the author implement:
    1. Popularity Recommendation *(Implemented in Home Page)*
    2. Content-based Recommendation *(Implemented in Recommendation Page : New User)*
    3. Collaborative Filtering *(Implemented in Recommendation Page : Existing User)*
    
    """
    st.info(about)

    st.divider()

    st.header('Methodology')
    method = """
    #### Popularity Recommendation
    Popularity Recommendation is a method that recommend the user top 5 most popular courses according to the highest number of subscribers.
    The more the number of subscribers is, that means, the highest the popularity of the course. So we recommend those first to the user. 
    This kind of recommendation is a general techniques used in other company such as Netflix (trending movies). And can be applied to New User or Existing User.

    #### Content-based Filtering
    This method recommends courses based on the similarity between course content and the user's preferences. 
    The algorithm analyzes the course metadata, such as titles, categories, and subcategories. 
    If a user liked courses related to machine learning, the system will recommend other courses that contain similar keywords and topics. 
    This kind of recommendation is called a personalized recommendation, since the recommendation comes from the user's preferences.

    #### Collaborative Filtering 
    This approach recommends courses based on the behavior and preferences of similar users. There are two types: user-based and item-based collaborative filtering. 
    1. User-based collaborative filtering finds users with similar interests and recommends courses that those users have liked. 
    2. Item-based collaborative filtering, finds courses that are often taken together and recommends them to the user. 
    
    This involves creating a user-item interaction matrix and applying techniques like matrix factorization or nearest neighbor algorithms to uncover patterns in user behavior.
    
    """
    st.info(method)

    st.divider()

    st.header('Room for Improvement')

    improvement = """
    There are some drawbacks in this implementation, which further can be improved in the future or by those who read this summary.
    1. What if a new user liked several courses, and becomes an existing user, then how can the recommendation applied to them? How the implementation using collaborative filtering instead?
    2. The model computation using collaborative filtering ends up with 5 gb size model, how to save the model with efficient size?
    3. The implementation here are using basic NLP techniques for Content-based, and KNN model using **Surprise** Library for Collaborative Filtering.
       These days, there are so many model implementation techniques which are more sophisticated. 
       So, the homework is implementing the recommendation using Deep Neural Network and Pyspark for Big Data Analysis.

    """
    st.info(improvement)
    st.divider()

if menu_id == 'Contact Me':
    
    st.title('About Me')
    st.divider()
    
    st.header('Author')

    author = """
    Hello, I'm Novita Fitriani. I graduated from Universitas Negeri Jakarta with major in Physics. After graduated, I worked in educational startup company CoLearn for 2+ years as a Physics QC Correctness. 
    During my study and career, I have been exposed with data analyzing which drives our overal company and business works, that's why I love and want to pursue data scientist. 
    I'm also looking to have a meaningful impact with my work and my interest lied more on the application side than just mere theory. 
    
    If you have any questions regarding this project, feel free to reach out to me in my social media below.

    Thank you for visiting my project!

    ---

    - **Gmail**     : [novitafitriani51@gmail.com](mailto:novitafitriani51@gmail.com)
    - **LinkedIn**  : [linkedin.com/in/novitafitriani/](https://www.linkedin.com/in/novitafitriani/)
    - **GitHub**    : [github.com/novitaftr](https://github.com/novitaftr)
    - **Website**   : [medium.com/@novitaftr](https://medium.com/@novitaftr)
    
    """

    st.info(author)

    st.divider()