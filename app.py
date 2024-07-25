import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

Technopole_template = go.layout.Template(
    layout_colorway=["#36A9E0", "#E5007D", "#144673", "#94C7EC", "#FFFFFF", "#333333", "#0E3449", "#015955"]
)
LABIA_template = go.layout.Template(
    layout_colorway=["#e2007d", "#852f85", "#4fb0ff", "#475297", "#FFFFFF", "#333333", "#0E3449", "#015955"]
)

def month_transformer(month_number):
    months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    return months[month_number - 1]


def day_of_week_transformer(day_number):
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    return days[day_number]


custom_order = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
interact_list = ['Clics',"J’aime","Commentaires",'Republications']

def rate_months(feature,df):
    sum = df.groupby('mois')[feature].sum()
    value = df.groupby('mois')[feature].sum().values[0]
    month_1 = sum.loc[df.groupby('mois')[feature].sum().index[1]]
    month_2 = sum.loc[df.groupby('mois')[feature].sum().index[0]]
    rate = ((month_2 - month_1) / month_1) * 100
    return value, rate

# Set page configuration
st.set_page_config(
     page_title="Linkedin Report App",
     page_icon="📈",
     initial_sidebar_state="auto",
     menu_items={
        'Get Help': 'mailto:kfox45@hotmail.fr',
        'Report a bug': "mailto:kfox45@hotmail.fr",
        'About': "#. This is an *extremely* cool app!"
    }
 )

def main():
    pages = {
            'ABONNES': ABO,
            'POSTS': POST,
            }

    if "page" not in st.session_state:
        st.session_state.update({
        # Default page
        'page': 'ABONNES'
        })

    with st.sidebar:
        st.title('LINKEDIN ANALYSER 📈')
        st.divider()
        page = st.selectbox("Selectionner une page", tuple(pages.keys()))
        theme = st.selectbox("Choisi un thème",("Lab'IA","Technopole"))
        if theme == "Lab'IA":
            pio.templates["temp"] = LABIA_template
        else:
            pio.templates["temp"] = Technopole_template
        st.divider()
    pages[page]()

    ########### ANALYSE ABONNEES #############

def ABO():
    
    st.title('Analyse des abonnés')
    st.divider()
    df2 = None
    # Télécharge les fichier   
    abonnee_file = st.file_uploader("Dépose ton fichier d'abonnée ici")
    if abonnee_file is not None:
        st.divider()
        df2 = pd.read_excel(abonnee_file)
        on = st.toggle("Selectionner toutes les années",value=False)
        if on:
            years = [2021, 2022, 2023, 2024, 2025]
        else:
            years = st.multiselect(
                    "Quelle(s) année(s) voulez vous analyser ?",
                    [2021, 2022, 2023, 2024, 2025],[2024]
                    )
        on2 = st.toggle("Selectionner tous les mois",value=True)
        if on2:
            months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        else:
            months = st.multiselect(
                    "Sélectionner deux mois à comparer",
                    ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],['Mai', 'Juin']
                    )
    st.divider()
    if df2 is not None:
        
        df2['annee'] = pd.DatetimeIndex(df2['Date']).year
        df2['mois'] = pd.DatetimeIndex(df2['Date']).month
        df2['jour'] = pd.DatetimeIndex(df2['Date']).day
        df2['jour_nom'] = pd.DatetimeIndex(df2['Date']).dayofweek
        df2['jour_nom'] = df2['jour_nom'].apply(day_of_week_transformer)
        df2['mois'] = df2['mois'].apply(month_transformer)
        df2['Date'] = pd.to_datetime(df2['Date'])
        df2_filtré = df2[(df2['annee'].isin(years)) & (df2['mois'].isin(months))]
        df_cat_month = df2_filtré.copy()
        df_cat_month['mois'] = pd.Categorical(df_cat_month['mois'], categories=custom_order, ordered=True)
        if on2:
            abonnés_total = df2['Total d’abonnés'].sum()
            st.metric(label = "Abonnés Total:", value = abonnés_total)
        elif len(months) == 2:  
            abonnee_sum = df2_filtré.groupby('mois')['Total d’abonnés'].sum()
            abonnee_value = df2_filtré.groupby('mois')['Total d’abonnés'].sum().values[0]
            abonnee_month_1 = abonnee_sum.loc[df2_filtré.groupby('mois')['Total d’abonnés'].sum().index[1]]
            abonnee_month_2 = abonnee_sum.loc[df2_filtré.groupby('mois')['Total d’abonnés'].sum().index[0]]
            abonnés_stats = ((abonnee_month_2 - abonnee_month_1) / abonnee_month_1) * 100

            st.metric(label = "Abonnés", value = abonnee_value, delta = f'{abonnés_stats:.2f} %') 
        else:
            st.warning('La comparaison se fait sur 2 mois.',icon="⚠️")
        fig = px.ecdf(df_cat_month, x="mois",
                   y="Total d’abonnés",
                   title = "Cumulé du nombre d'abonnée",
                   template = 'temp',
                   ecdfnorm=None
                   )                
        fig.update_layout(autosize = True,
                        title_x = 0.5,
                        margin=dict(l=50,r=50,b=50,t=50,pad=4),
                        xaxis_title = '',
                        yaxis_title = '',
                        yaxis = {'visible': True},
                        template = 'plotly_dark'
                        )
        fig.update_xaxes(tickfont_size=15,tickmode='linear')  
        st.plotly_chart(fig) 


    ########### ANALYSE POSTS #############

def POST():
    st.title('Analyse des posts')
    df = None
    st.divider()
    posts_file = st.file_uploader("Dépose ton fichier de posts ici")
    if posts_file is not None:
        df = pd.read_csv(posts_file, delimiter=';', skiprows=0, low_memory=False, decimal=',')
        on = st.toggle("Selectionner toutes les années",value=False)
        if on:
            years = [2021, 2022, 2023, 2024, 2025]
        else:
            years = st.multiselect(
                    "Quelle(s) année(s) voulez vous analyser ?",
                    [2021, 2022, 2023, 2024, 2025],[2024]
                    )
        on2 = st.toggle("Selectionner tous les mois",value=True)
        if on2:
            months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        else:
            months = st.multiselect(
                    "Sélectionner deux mois à comparer",
                    ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],['Mai', 'Juin']
                    )
    if df is not None:
        df['annee'] = pd.DatetimeIndex(df['Date de création']).year
        df['mois'] = pd.DatetimeIndex(df['Date de création']).month
        df['jour'] = pd.DatetimeIndex(df['Date de création']).day
        df['jour_nom'] = pd.DatetimeIndex(df['Date de création']).dayofweek
        df['jour_nom'] = df['jour_nom'].apply(day_of_week_transformer)
        df['mois'] = df['mois'].apply(month_transformer)
        df['Date de création'] = pd.to_datetime(df['Date de création'])
        df['Interactions'] = df['Clics'] + df["J’aime"] + df["Commentaires"] + df['Republications']
        df_filtré = df[(df['annee'].isin(years)) & (df['mois'].isin(months))]
        st.divider()
        col1, col2, col3, col4 = st.columns(4)


        # POST PUBLIE

        with col1:
            if on2:
                posts_total = df.shape[0]
                st.metric(label = "Posts publiés total:", value = posts_total)
            elif len(months) == 2:  
                monthly_counts = df_filtré.groupby('mois').size().reset_index(name='LineCount')
                posts_month_last = df_filtré.groupby('mois').size()[0]
                monthly_counts['LineCountChange'] = monthly_counts['LineCount'].diff()
                monthly_counts['RateOfChange'] = -(monthly_counts['LineCountChange'] / monthly_counts['LineCount'].shift(1)) * 100
                rate_of_change = monthly_counts.iloc[1]['RateOfChange']
                st.metric(label = "Post publiés", value = posts_month_last, delta = f'{rate_of_change:.2f} %') 
            else:  
                st.warning('La comparaison se fait sur 2 mois.',icon="⚠️")
            with st.expander("Type de contenu"):
                contenu_type_ratio = (df['Type de contenu'].value_counts(normalize=True)*100).rename_axis('ratio').reset_index(name='counts')
                fig = px.pie(contenu_type_ratio,
                    values='counts',
                    names='ratio', 
                    color ='ratio',
                    title='Proportion des types de contenu',
                    width= 1000,
                    hole=0.5,
                    template = 'temp',
                    )
                fig.update_traces(textposition = 'outside', textfont_size = 15)             
                fig.update_layout(title_x = 0.5,
                                autosize = True, 
                                margin=dict(l=50,r=50,b=50,t=50,pad=4),
                                template = 'plotly_dark' )                
                st.plotly_chart(fig)

        # IMPRESSIONS


        with col2:
            if on2:
                impressions_total = df['Impressions'].sum()
                st.metric(label = "Impressions total:", value = impressions_total)
            elif len(months) == 2:  
                impressions_sum = df_filtré.groupby('mois')['Impressions'].sum()
                impressions_value = df_filtré.groupby('mois')['Impressions'].sum().values[0]
                impressions_month_1 = impressions_sum.loc[df_filtré.groupby('mois')['Impressions'].sum().index[1]]
                impressions_month_2 = impressions_sum.loc[df_filtré.groupby('mois')['Impressions'].sum().index[0]]
                impressions_stats = ((impressions_month_2 - impressions_month_1) / impressions_month_1) * 100

                st.metric(label = "Impréssions", value = impressions_value, delta = f'{impressions_stats:.2f} %') 
            else:
                st.warning('La comparaison se fait sur 2 mois.',icon="⚠️")
       

        # INTERACTIONS

        with col3:
            if on2:
                Interaction_total = df['Interactions'].sum()
                st.metric(label = "Interactions total:", value = Interaction_total)
                with st.expander('Détails'):
                    for i in interact_list:
                        Interaction_total = df[i].sum()
                        st.metric(label = i, value = Interaction_total)
            elif len(months) == 2:  
                interactions_sum = df_filtré.groupby('mois')['Interactions'].sum()
                interactions_value = df_filtré.groupby('mois')['Interactions'].sum().values[0]
                interaction_month_1 = interactions_sum.loc[df_filtré.groupby('mois')['Interactions'].sum().index[1]]
                interaction_month_2 = interactions_sum.loc[df_filtré.groupby('mois')['Interactions'].sum().index[0]]
                interactions_stats = ((interaction_month_2 - interaction_month_1) / interaction_month_1) * 100
                st.metric(label = "Intéractions", value = interactions_value, delta = f'{interactions_stats:.2f} %') 
                with st.expander('Détails'):
                    for i in interact_list:
                        value, rate = rate_months(i,df_filtré)
                        st.metric(label = i, value = value, delta = f'{rate:.2f} %')
            else:
                st.warning('La comparaison se fait sur 2 mois.',icon="⚠️")
            
            

        # Taux d'engagement     
        
        with col4:
            if on2:
                taux_engagement__total = df['Taux d’engagement'].mean()
                st.metric(label = "Taux d'engagement total:", value = f'{taux_engagement__total:.3f}' )
            elif len(months) == 2:  
                engagement_mean = df_filtré.groupby('mois')['Taux d’engagement'].mean()
                engagement_value = df_filtré.groupby('mois')['Taux d’engagement'].mean().values[0]
                engagement_month_1 = engagement_mean.loc[df_filtré.groupby('mois')['Taux d’engagement'].mean().index[1]]
                engagement_month_2 = engagement_mean.loc[df_filtré.groupby('mois')['Taux d’engagement'].mean().index[0]]
                engagement_stats = ((engagement_month_2 - engagement_month_1) / engagement_month_1) * 100

                st.metric(label = "Taux d'engagement", value = f'{engagement_value:.2f}', delta = f'{engagement_stats:.2f} %') 
            else:
                st.warning('La comparaison se fait sur 2 mois.',icon="⚠️")

            with st.expander('Format de posts'):
                data_ratio_post_format = (df['format de Post'].value_counts(normalize=True)*100).rename_axis('ratio').reset_index(name='counts')
                fig = px.pie(data_ratio_post_format ,
                    values='counts',
                    names='ratio', 
                    color ='ratio',
                    title='Proportion des formats de post',
                    width= 1000,
                    hole=.5,
                    template = 'temp',
                    )
                fig.update_traces(textposition = 'outside', textfont_size = 15)             
                fig.update_layout(title_x = 0.5,
                                autosize = True,          
                                margin=dict(l=50,r=50,b=50,t=50,pad=4),
                                template = 'plotly_dark' )
                st.plotly_chart(fig)

        # TOP 3
        st.divider()
        col_1, col_2 = st.columns(2)
        with col_1:
            TOP3_impressions_index = list(df['Impressions'].sort_values(ascending=False).index)[:3]
            df_top3_posts_view_rate = df.iloc[TOP3_impressions_index]
            Top3_liste = list(df_top3_posts_view_rate['Publier le lien'].values)
            st.title("TOP VUS")
            medals = ['🥇','🥈','🥉']
            for i, medal in zip(Top3_liste[:3], medals):
                st.write(f'{medal} {i}')
        with col_2:
            TOP3_engagment_rate_index = list(df['Taux d’engagement'].sort_values(ascending=False).index)[:3]
            df_top3_engagement_rate = df.iloc[TOP3_engagment_rate_index]
            Top3_liste = list(df_top3_engagement_rate['Publier le lien'].values)
            st.title("TOP ENGAGEANT")
            medals = ['🥇','🥈','🥉']
            for i, medal in zip(Top3_liste[:3], medals):
                st.write(f'{medal} {i}')



if __name__ == "__main__":
    main()