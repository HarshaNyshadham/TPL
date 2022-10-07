from turtle import title
import pandas as pd
from plotly import graph_objects as go
from plotly import express as px
from plotly.subplots import make_subplots



def playerDistribution(df):
    

    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }

    df=df.sort_values(by=["%Win","%Games"])
    # print(plotDf)
    fig = px.scatter(df,x="%Games", y="%Win",color="%Win",size="%Games",hover_data=['Player','Win','Loss','Games Won','Games Loss'],
                        text='Player',template='plotly_white')

    fig.update_xaxes(type='category',categoryorder='category ascending')
    fig.update_traces(textposition='top center',textfont_size=10)
    fig.update_layout(xaxis=dict(
            minor=dict(showgrid=True),
            rangeselector=dict(activecolor='#ff0000'),
            rangeslider=dict(visible=True,autorange=True,bgcolor="aliceblue",bordercolor="hotpink",borderwidth=1),
            type="category",
            
        ))
    fig.add_shape(type="rect",
    xref="x", yref="y",
    x0=0, y0=0,
    x1=32, y1=20,
    opacity=0.1,
    fillcolor="blue",
    line_color="blue",
    
    )
    fig.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, y0=20,
        x1=32, y1=40,
        opacity=0.1,
        fillcolor="purple",
        line_color="purple",
        
    )
    fig.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, y0=40,
        x1=32, y1=60,
        opacity=0.1,
        fillcolor="pink",
        line_color="pink",
        
    )
    fig.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, y0=60,
        x1=32, y1=80,
        opacity=0.1,
        fillcolor="orange",
        line_color="orange",
        
    )
    fig.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, y0=80,
        x1=32, y1=100,
        opacity=0.1,
        fillcolor="yellow",
        line_color="yellow",
        
    )
    font=dict(family="Courier New, monospace",
                size=12,
                color="black"
                )
    fig.add_annotation(x=28,y=10,text='Just Chilling 😎',showarrow=False,font=font)
    fig.add_annotation(x=28,y=30,text='The Tireless 🏃🏻',showarrow=False,font=font)
    fig.add_annotation(x=28,y=50,text='The Heavyweights 🏋',showarrow=False,font=font)
    fig.add_annotation(x=2,y=70,text='The Pros 🙂',showarrow=False,font=font)
    fig.add_annotation(x=2,y=90,text='The Legends 😇',showarrow=False,font=font)
    #fig.layout.update(sliders=newdf['%Games'])
    
    return fig

def playerBagelPlot(df,player):
    
    pindex=df.loc[df['Player']==player].index.values[0]
    gotBagels=eval(df.loc[pindex]['gotBagels'])
    Bageled=eval(df.loc[pindex]['Bagels'])
    #print(gotBagels,Bageled)
    taken=[]
    given=[]
    count=[0,1,1]

    #first taken then given
    for item in gotBagels:
        taken.append(item)
        count.append(gotBagels[item])
    for item in Bageled:
        given.append(item)
        count.append(Bageled[item])
    
    temp_parent=['taken' for value in taken]+['given' for value in given]
    #replace count for taken and given from 1
    count[1]=len(taken)
    count[2]=len(given)
    
    #print(taken,given)

    fig =go.Figure(go.Sunburst(
        
        labels=[ "Bagels","taken","given"]+taken+given,
        parents=["","Bagels","Bagels"]+temp_parent,
        values=count,
    ))
    # print([ "Bagels","taken","given"]+taken+given)
    # print(["","Bagels","Bagels"]+temp_parent)
    # print(count)
    fig.update_layout(title=str(player)+' Bagel stat')
    return fig

def PlayerWinPlot(df,player):
    pindex=df.loc[df['Player']==player].index.values[0]
    Win=eval(df.loc[pindex]['WinList'])
    Loss=eval(df.loc[pindex]['LossList'])

    Player=[]
    WinPerc=[]
    TotalGames=[]


    for item in Win:
        Player.append(item)
        
    for item in Loss:
        if item not in Player:
            Player.append(item)

    

    for p in Player:
        if p in Win:
            
            if p in Loss:
                WinPerc.append(str(int(Win[p]/(Win[p]+Loss[p])*100))+'%')
                TotalGames.append(Win[p]+Loss[p])
            else:
                WinPerc.append('100%')
                TotalGames.append(Win[p])
        else:
            
            WinPerc.append('0%')
            TotalGames.append(Loss[p])

    

    Parent=['Win%' for value in range(0,len(Player))]
    
    # print(Player,WinPerc,Parent) 
    # print(len(Player),len(WinPerc),len(Parent)) 

    sbdf=pd.DataFrame(dict(Parent=Parent,Player=Player,Value=WinPerc,TotalGames=TotalGames))
    # sbdf=sbdf.sort_values(by=['Value'])
    #print(sbdf)
    
    fig=px.sunburst(sbdf, path=['Parent', 'Value','Player'], values='TotalGames',color='Value',color_continuous_scale ="Emrld")
    fig.update_layout(title=str(player)+' Win stat')
    
    
   
    
    return fig


def playerMacthesPlot(player):
    df=pd.read_excel(r'rawdata.xlsx', engine ='openpyxl',keep_default_na=False)
    playerDF=df[df['Player1']==player].append(df[df['Player2']==player])
    #print(playerDF)

    tableDf=pd.DataFrame(columns=['Player','Score','Season','Color'])
    for index,row in playerDF.iterrows():
        tableDf.at[index,'Score']=row['Score']
        tableDf.at[index,'Season']=row['Season']
        if(row['Player1']==player):
            tableDf.at[index,'Player']=row['Player2']
        elif(row['Player2']==player):
            tableDf.at[index,'Player']=row['Player1']

        if(row['Winner']==player):
            tableDf.at[index,'Color']='lavender'
        else:
            tableDf.at[index,'Color']='salmon'
    #print(tableDf)
    tableDf=tableDf.sort_values(by=['Color','Season'],ascending=[True,False])
    fig = go.Figure(data=[go.Table(
    header=dict(values=['Player','Score','Season'],
                fill_color='cadetblue',
                align='left'),
    cells=dict(values=[tableDf.Player, tableDf.Score, tableDf.Season],
               fill_color=[tableDf.Color],
               align='left'))
    ])
    fig.update_layout(title=str(player)+' vs - past macthes')
    return fig
# df=pd.read_excel(r'plotdata.xlsx', engine ='openpyxl',keep_default_na=False)
# fig1=playerBagelPlot(df,"Aditya")
# fig2=playerDistribution(df)

# fig = make_subplots()
# #fig.add_trace(fig1.data[0])
# fig.add_trace(fig2.data[0])
# fig.show()
# #print(fig1.data)