import streamlit as st
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.header('Olympic Analysis')
user_menu= st.sidebar.radio(

    'Slect an Option',
    ('Medal Tally','Overall Analysis','Cuntry-wise Analysis','Athlete wise Analysis')
)

#meadl Telly

if user_menu == 'Medal Tally':
    
    year,country=helper.cot_year(df)

    select_year=st.sidebar.selectbox('Select Year',year)
    select_country=st.sidebar.selectbox('Select Country',country)

    if select_year=='Overall' and select_country=='Overall':
        st.title("Medal Telly")
    
    if select_year!='Overall' and select_country =='Overall':
        st.title(f"Medal Telly of Olympic year {str(select_year)}")
    
    if select_year=='Overall' and select_country !='Overall':
        st.title(f"Medal Telly of  {str(select_country)} in Overall Olympics" )
    
    if select_year!='Overall' and select_country !='Overall':
        st.title(f"Medal Telly of {select_country} in {str(select_year)}'s Olympic" )
    madel_telly= helper.performance(df,select_year,select_country)
    st.table(madel_telly)

if user_menu == 'Overall Analysis':
    

    editions=df['Year'].sort_values().unique().shape[0]
    City=df['City'].sort_values().unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].dropna().sort_values().unique().shape[0]

    st.title('Top Statistics')

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("City")
        st.title(City)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    nations_over_time=helper.data_over_time(df,'region')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10,5))
    x=nations_over_time['Year']
    y=nations_over_time['count']
    sns.lineplot(x=x,y=y,)
    plt.title('Participating nations over time')
    plt.ylabel('Nation Count')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot()
    nations_over_time=helper.data_over_time(df,'Event')


    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10,5))
    x=nations_over_time['Year']
    y=nations_over_time['count']
    sns.lineplot(x=x,y=y,)
    plt.title('Total Events over time')
    plt.ylabel('Event Count')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot()

    st.title('No  of Events over time(Every Sports)')
    x=df.drop_duplicates(['Year','Event','Sport'])
    st.set_option('deprecation.showPyplotGlobalUse',False)
    plt.figure(figsize=(20,20))
    sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot()

    sports=helper.top_athletes(df)
    sle_sports=st.selectbox("",sports)

    
    if  sle_sports=='Overall':
        st.title("Overall Top Athletes")
        temp=df.groupby(['Name','region','Sport'])[['Bronze','Gold','Silver']].sum().reset_index()
        temp['medals']=temp['Gold']+temp['Silver']+temp['Bronze']
        temp=temp.drop(['Bronze','Gold','Silver'],axis=1).sort_values('medals',ascending=False)
        st.table(temp.head(10))
    else:
        st.title(f"Top Athletes in {sle_sports}")
        temp=df.groupby(['Name','region','Sport'])[['Bronze','Gold','Silver']].sum().reset_index()
        temp=temp[temp['Sport']==sle_sports]
        temp['medals']=temp['Gold']+temp['Silver']+temp['Bronze']
        temp=temp.drop(['Bronze','Gold','Silver'],axis=1).sort_values('medals',ascending=False)
        st.table(temp.head(10))

if user_menu == 'Cuntry-wise Analysis':

    st.header('Cuntry-wise Analysis')

    year,country=helper.cot_year(df)
    select_country=st.sidebar.selectbox('Select Country',country)

    
    if select_country != "Overall":
        temp_df=df.dropna(subset=['Medal'])
        temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal','region'])
        temp_df=temp_df[temp_df['region']==select_country]
        temp_df=temp_df.groupby(['Year']).count()['Medal'].reset_index()

        st.title(f"{select_country}'s Medal Tally Graph for over the years")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        sns.lineplot(data=temp_df,x='Year',y='Medal',color='red')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot()

    else:

        temp_df=df.dropna(subset=['Medal'])
        temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal','region'])
        temp_df=temp_df[temp_df['region']==select_country]
        temp_df=temp_df.groupby(['Year']).count()['Medal'].reset_index()
        st.title('Select The Country from the drop-down')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        sns.lineplot(data=temp_df,x='Year',y='Medal',color='red')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot()
    
    st.title("Sports In Whcich A country's' good at")

    if  select_country != "Overall":

        st.title(f"{select_country} exceles in fthe following sports")
        temp_df=df.dropna(subset=['Medal'])
        temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal','region'])
        temp_df=temp_df[temp_df['region']==select_country]
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.figure(figsize=(20,20))
        sns.heatmap(temp_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0),annot=True)
        st.pyplot()
    else:

        temp_df=df.dropna(subset=['Medal'])
        temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal','region'])
        temp_df=temp_df[temp_df['region']=='USA']
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.figure(figsize=(20,20))
        sns.heatmap(temp_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0),annot=True)
        st.pyplot()
    
    
    st.title("Top Atheletes of Country")


    if  select_country=='Overall':
        st.title("Overall Top Athletes")
        temp=df.groupby(['Name','region','Sport'])[['Bronze','Gold','Silver']].sum().reset_index().drop_duplicates()
        temp['medals']=temp['Gold']+temp['Silver']+temp['Bronze']
        temp=temp.drop(['Bronze','Gold','Silver'],axis=1).sort_values('medals',ascending=False)
        st.table(temp.head(10))
    else:
        st.title(f"Top Athletes in {select_country}")
        temp=df.groupby(['Name','region','Sport'])[['Bronze','Gold','Silver']].sum().reset_index().drop_duplicates()
        temp=temp[temp['region']==select_country]
        temp['medals']=temp['Gold']+temp['Silver']+temp['Bronze']
        temp=temp.drop(['Bronze','Gold','Silver'],axis=1).sort_values('medals',ascending=False)
        st.table(temp.head(10))
        
if user_menu =='Athlete wise Analysis':
    
    st.header('Athlete wise Analysis')

    st.title('Cances of winning a medal on the bases of age')

    x1,x2,x3,x4=helper.winning_age(df)
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalest','Silver Medalist',"Bronze Medalist"],show_hist=False,show_rug=False)
    st.plotly_chart(fig)

    st.title('Cances of winning a medal on the bases of age')

    sports=helper.top_athletes(df)
    sle_sports=st.selectbox("select Sports",sports)

    h_w_df=helper.hight_wight_data(df,sle_sports)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    ax=sns.scatterplot(data=h_w_df,y='Height',x='Weight',hue='Medal',style='Sex')
    st.pyplot()

    st.title('Gender difference over the years')

    gend_df=helper.gender_dif(df)
    fig = px.line(gend_df, x='Year', y=['Male', 'Female'],
              title='Male and Female Trends Over Time',
              labels={'value': 'Count', 'variable': 'Gender'})
    st.plotly_chart(fig)
