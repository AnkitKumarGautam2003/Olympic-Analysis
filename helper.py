'''def medal_tally(df):

    medal_tally=df.drop_duplicates(['region','Games','Year','Season','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False)

    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    medal_tally['Gold']=medal_tally['Gold'].astype(int)
    medal_tally['Silver']=medal_tally['Silver'].astype(int)
    medal_tally['Bronze']=medal_tally['Bronze'].astype(int)
    medal_tally['total']=medal_tally['total'].astype(int)

    return medal_tally'''
import pandas as pd

def cot_year(df):

    year=years=df['Year'].sort_values().unique().tolist()
    years.insert(0,'Overall')

    country=countrys=sorted(df['region'].dropna().unique().tolist())
    countrys.insert(0,'Overall')

    return year,country

def performance(df,year,country):
    medal_df=df.drop_duplicates(['region','Games','Year','Season','City','Sport','Event','Medal'])
    spicel_case=0
    if year=='Overall' and country =="Overall":
        temp_df=medal_df

    if year=='Overall' and country !='Overall':
        temp_df=medal_df[medal_df['region']==str(country)]
        spicel_case=1
    if year!='Overall' and country =='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]

    if year!='Overall' and country !='Overall':
        temp_df=df=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==str(country))]

    if spicel_case==0:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        x['total']=x['Gold']+x['Silver']+x['Bronze']
    else:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
        x['total']=x['Gold']+x['Silver']+x['Bronze']
    x['Gold']=x['Gold'].astype(int)
    x['Silver']=x['Silver'].astype(int)
    x['Bronze']=x['Bronze'].astype(int)
    x['total']=x['total'].astype(int)

    return x

def data_over_time(df,col):
    
    no_of_nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')

    return no_of_nations_over_time

def top_athletes(df):
    sports=df['Sport'].unique().tolist()
    sports.insert(0,'Overall')
    return sports

def winning_age(df):
    atheleate_df=df.drop_duplicates(['Name','region'])
    x1=atheleate_df['Age'].dropna()
    x2=atheleate_df[atheleate_df['Medal']=='Gold']['Age'].dropna()
    x3=atheleate_df[atheleate_df['Medal']=='Silver']['Age'].dropna()
    x4=atheleate_df[atheleate_df['Medal']=='Bronze']['Age'].dropna()

    return x1,x2,x3,x4

def hight_wight_data(df,sport):

    ath_df=df.drop_duplicates(subset=['Name','region'])
    ath_df['Medal'].fillna('NO_medals',inplace=True)
    if sport!='Overall':
        tem_df=ath_df[ath_df['Sport']==sport]
        return tem_df
    else:
        return ath_df

def gender_dif(df):
    ged_df=df.drop_duplicates(subset=['Name','Sex'])
    male=ged_df[ged_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    femail=ged_df[ged_df['Sex']!='M'].groupby('Year').count()['Name'].reset_index()
    final_df=male.merge(femail,on='Year',how='left')
    final_df.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final_df.fillna(0,inplace=True)

    return final_df