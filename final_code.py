# IMPORTING LIBRARIES
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob # for sentiment analysis
from collections import Counter
import plotly.graph_objects as go

theme = 'plotly_dark'

# STARTING DASH
app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#2A363B','color': 'white','fontFamily':'verdana','textAlign':'center','border': '5px solid white',
                                'paddingLeft': '250px','paddingRight': '250px','paddingTop': '70px','paddingBottom': '50px'},
    children= [

    html.H1(style={'fontFamily':'Chromoxome Pro','fontSize':'400%'},children='TV SHOW / MOVIE ANALYSIS DASHBOARD'),
    html.H4(style={'fontFamily':'Chromoxome Pro','fontSize':'115%', 'paddingLeft': '250px','paddingRight': '250px'},children=
        dcc.Markdown('''
            _The dialogue exchange data for all the TV shows/movies is scraped from Transcripts Wiki | Fandom using
            BeautifulSoup. This dashboard is created using Dash for python. Dash is
            built over Flask, React & Plotly._

            ''')),
    html.Div(children=html.H1(style={'fontFamily':'Chromoxome Pro'},children='''
        Choose the show/movie:
    ''')),
    html.H5(style={'color':'black'},children=
    dcc.Dropdown(
        id='input',
        options=[ # CREATING DROP DOWN LIST
            {'label': 'Brooklyn 9 9 : Pilot', 'value': 'Pilot'},
            {'label': 'Brooklyn 9 9 : Boyles Hunch', 'value': 'Boyles Hunch'},
            {'label': 'Brooklyn 9 9 : Halloween III', 'value': 'Halloween III'},
            {'label': 'Brooklyn 9 9 : New Captain', 'value': 'New Captain'},
            {'label': 'Brooklyn 9 9 : The Funeral', 'value': 'The Funeral'},
            {'label': 'Brooklyn 9 9 : The Oolong Slayer', 'value': 'The Oolong Slayer'},
            {'label': 'F.R.I.E.N.D.S', 'value': 'FRIENDS'},
            {'label': 'Avengers - Infinity War', 'value': 'Avengers-Infinity War'},
            {'label': 'Avengers - Endgame', 'value': 'Avengers-Endgame'},
            {'label': 'Spiderman - Homecoming', 'value': 'Spiderman-Homecoming'},
            {'label': 'Spiderman - Far From Home', 'value': 'Spiderman-Far From Home'},
            {'label': 'Sonic The Hedgehog (2020)', 'value': 'Sonic The Hedgehog (2020)'},
            {'label': 'SpongeBob SquarePants (1999)', 'value': 'SpongeBob SquarePants (1999)'},
            {'label': 'Toy Story 3', 'value': 'Toy Story 3'},
            {'label': 'The Simpsons', 'value': 'The Simpsons'},
        ],value = 'Pilot')),
    html.Div(id='output-graph5'),
    html.Div(id='output-graph'),
    html.Div(id='output-graph2'),
    html.Div(id='output-graph3'),
    html.Div(id='output-graph4'),
    html.Div(id='output-graph7'),
    html.Div(id='output-graph8'),
    html.Div(style={'fontFamily':'Chromoxome Pro','fontSize':'100%','paddingTop':'70px'},children=['> created as a final project for EE551 by Akash Negi <'])
        ])


#GRAPH 1
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    path = 'datasets/'+str(input_data)+'.csv'
    df = pd.read_csv(path, encoding='unicode_escape', names = ['Cast','Dialogue'])
    df_most_lines = pd.DataFrame(df['Cast'].value_counts()).iloc[:7]
    df_most_lines=df_most_lines.reset_index()
    df_most_lines.columns = ['Cast','Lines']
    

    return dcc.Graph(
        figure=go.Figure(data=go.Bar(x=df_most_lines.Cast,y=df_most_lines.Lines, name='input_data', marker=dict(color = '#E84A5F')),
                        layout=dict(template=theme,title='WHO USED THE MOST LINES?',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'))



        )
      



#GRAPH 2
@app.callback(
    Output(component_id='output-graph2', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    path = str(input_data)+'.csv'
    df = pd.read_csv(path, encoding='unicode_escape', names = ['Cast','Dialogue'])
    df['word_count'] = df['Dialogue'].str.split().str.len()


    return dcc.Graph(

                        figure=go.Figure(data=go.Bar(x=df.Cast,y=df.word_count, name='input_data',marker=dict(color='#FECEAB')),
                        layout=dict(template=theme,title='WHO USED THE MOST WORDS ON AVERAGE?',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'))


                    )
    



#GRAPH 3
@app.callback(
    Output(component_id='output-graph3', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    path = str(input_data)+'.csv'
    df = pd.read_csv(path, encoding='unicode_escape', names = ['Cast','Dialogue'])
    df['word_count'] = df['Dialogue'].str.split().str.len()
    total_sum = df.groupby(['Cast'])['word_count'].sum().reset_index()
    total_sum = total_sum.sort_values(by='word_count', ascending=False)


    return dcc.Graph(

        figure=go.Figure(data=go.Bar(x=total_sum.Cast,y=total_sum.word_count, name='input_data',marker=dict(color='#99B898')),
                        layout=dict(template=theme,title='WHO USED THE MOST WORDS IN TOTAL?',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'))

        )
     





#GRAPH 4
@app.callback(
    Output(component_id='output-graph4', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    path = str(input_data)+'.csv'
    df = pd.read_csv(path, encoding='unicode_escape', names = ['Cast','Dialogue'])
    df['word_count'] = df['Dialogue'].str.split().str.len()
    total_sum = df.groupby(['Cast'])['word_count'].sum().reset_index()
    total_sum = total_sum.sort_values(by='word_count', ascending=False)

    # Clean and Normalize Text
    #tokenize, lowercase, remove punctuation, remove alphanumeric characters, remove stopwords
    from nltk.corpus import stopwords
    stopwords = set(stopwords.words('english'))

    def clean(text):
        text = word_tokenize(str(text))
        text = [word.lower() for word in text]
        punct = str.maketrans('', '', string.punctuation) 
        text = [word.translate(punct) for word in text] 
        text = [word for word in text if word.isalpha()]
        text = [word for word in text if not word in stopwords]
        return " ".join(text)

    df['clean_text'] = df['Dialogue'].apply(clean)

    # Create Word Count Column for Clean Text

    df['clean_word_count'] = df['clean_text'].str.split().str.len()


    return dcc.Graph(

         figure=go.Figure(data=go.Bar(x=df.Cast,y=df.clean_word_count, marker=dict(color='#FF847C')),
                        layout=dict(template=theme,title='WHO USED THE MOST CLEAN WORDS?',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'))


        )
      




#GRAPH 5
@app.callback(
    Output(component_id='output-graph5', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    path = str(input_data)+'.csv'
    df = pd.read_csv(path, encoding='unicode_escape', names = ['Cast','Dialogue'])
    df['word_count'] = df['Dialogue'].str.split().str.len()
    total_sum = df.groupby(['Cast'])['word_count'].sum().reset_index()
    total_sum = total_sum.sort_values(by='word_count', ascending=False)


    from nltk.corpus import stopwords
    stopwords = set(stopwords.words('english'))

    def clean(text):
        text = word_tokenize(str(text))
        text = [word.lower() for word in text]
        punct = str.maketrans('', '', string.punctuation) 
        text = [word.translate(punct) for word in text] 
        text = [word for word in text if word.isalpha()]
        text = [word for word in text if not word in stopwords]
        return " ".join(text)

    df['clean_text'] = df['Dialogue'].apply(clean)

    # Create Word Count Column for Clean Text

    df['clean_word_count'] = df['clean_text'].str.split().str.len()

    #Apply Sentiment Polarity to Text with TextBlob

    df['polarity'] = [round(TextBlob(word).sentiment.polarity, 2) for word in df['clean_text']]
    df['sentiment'] = ['Positive' if polarity > 0 
                                 else 'Negative' if polarity < 0 
                                     else 'Neutral' 
                                         for polarity in df['polarity']]

    sent = pd.DataFrame(df.sentiment.value_counts())
    sent = sent.reset_index()
    sent.columns = ['Sentiment','Count']


    return dcc.Graph(

        figure=go.Figure(data=go.Pie(values=sent.Count, labels=sent.Sentiment),
                        layout=dict(template=theme,title='OVERALL SENTIMENT ANALYSIS OF THE SHOW',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'))

        )
    





#GRAPH 6
@app.callback(
    Output(component_id='output-graph7', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    path = str(input_data)+'.csv'
    df = pd.read_csv(path, encoding='unicode_escape', names = ['Cast','Dialogue'])
    df['word_count'] = df['Dialogue'].str.split().str.len()
    total_sum = df.groupby(['Cast'])['word_count'].sum().reset_index()
    total_sum = total_sum.sort_values(by='word_count', ascending=False)

    from nltk.corpus import stopwords

    stopwords = set(stopwords.words('english'))

    def clean(text):
        text = word_tokenize(str(text))
        text = [word.lower() for word in text]
        punct = str.maketrans('', '', string.punctuation) 
        text = [word.translate(punct) for word in text] 
        text = [word for word in text if word.isalpha()]
        text = [word for word in text if not word in stopwords]
        return " ".join(text)

    df['clean_text'] = df['Dialogue'].apply(clean)

    # Create Word Count Column for Clean Text

    df['clean_word_count'] = df['clean_text'].str.split().str.len()


    # Build a counter function to count words

    def counter(text):
        cnt = Counter()
        for msgs in text:
            for msg in msgs:
                cnt[msg] += 1
        return cnt

    import sys

    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")


    person = (str(df.Cast.value_counts()).strip().split(' ')[0])
    max_words = df.groupby('Cast')
    max_words = max_words.get_group(person)
    max_words['clean_text'] = max_words['clean_text'].apply(lambda x: word_tokenize(x))
    text_cnt = counter(max_words['clean_text'])
    j = text_cnt.most_common()

    j = pd.DataFrame(j, columns = ['Words', 'Counts'])
    j = j.sort_values(by='Counts', ascending=False)[:20]

    return dcc.Graph(


         figure=go.Figure(data=go.Bar(x=j.Words,y=j.Counts, name='input_data',marker=dict(color='#E84A5F')),
                        layout=dict(template=theme,title='MOST COMMON WORDS OF CHARACTER WITH MOST LINES - ' + person,paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'))

        )
       





#GRAPH 7
@app.callback(
    Output(component_id='output-graph8', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    path = str(input_data)+'.csv'
    df = pd.read_csv(path, encoding='unicode_escape', names = ['Cast','Dialogue'])
    df['word_count'] = df['Dialogue'].str.split().str.len()
    total_sum = df.groupby(['Cast'])['word_count'].sum().reset_index()
    total_sum = total_sum.sort_values(by='word_count', ascending=False)

    from nltk.corpus import stopwords

    stopwords = set(stopwords.words('english'))

    def clean(text):
        text = word_tokenize(str(text))
        text = [word.lower() for word in text]
        punct = str.maketrans('', '', string.punctuation) 
        text = [word.translate(punct) for word in text] 
        text = [word for word in text if word.isalpha()]
        text = [word for word in text if not word in stopwords]
        return " ".join(text)

    df['clean_text'] = df['Dialogue'].apply(clean)

    # Create Word Count Column for Clean Text

    df['clean_word_count'] = df['clean_text'].str.split().str.len()


    # Build a counter function to count words

    def counter(text):
        cnt = Counter()
        for msgs in text:
            for msg in msgs:
                cnt[msg] += 1
        return cnt

    import sys

    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")


    person2 = (str(df.Cast.value_counts()).strip().split('\n')[1]).strip().split(' ')[0]
    max_words = df.groupby('Cast')
    max_words = max_words.get_group(person2)
    max_words['clean_text'] = max_words['clean_text'].apply(lambda x: word_tokenize(x))
    text_cnt = counter(max_words['clean_text'])
    l = text_cnt.most_common()

    l = pd.DataFrame(l, columns = ['Words', 'Counts'])
    l = l.sort_values(by='Counts', ascending=False)[:20]

    return dcc.Graph(

         figure=go.Figure(data=go.Bar(x=l.Words,y=l.Counts, name='input_data',marker=dict(color='#99B898')),
                        layout=dict(template=theme,title='MOST COMMON WORDS OF CHARACTER WITH 2ND MOST LINES - ' + person2,paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'))

        )
        



# RUN THE APP

if __name__ == '__main__':
    app.run_server(debug=True)


