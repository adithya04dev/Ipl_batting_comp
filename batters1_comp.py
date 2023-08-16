
import pandas as pd
import numpy as np
import pickle
df=pd.read_csv("processed_ballbyball.csv")

class Batter_comp():
    
    def __init__(self,deliveries_df):
        
        self.df = deliveries_df.copy()
        self.players = self.df['batter'].unique()
        self.dic={1:[i for i in range(0,6)],2:[i for i in range(6,11)],3:[i for i in range(11,16)],4:[i for i in range(16,21)]}
        

    def calculate(self,overs1,BowlingType,Season,limit):
        
            overs=[]
            for over in overs1:
                overs=overs+self.dic[over]
                
            
            
            batsman_df = pd.DataFrame(columns=['player_name','total_runs','outs','balls_played','average_runs','strike_rate','bpercent','dpercent'])
            dis=["run out", 'retired hurt',  'obstructing the field','retired out']
            
            players=self.df.loc[(self.df['Season'].isin(Season)) & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs)) ]['batter'].unique()
            
            for player in players:
            
                run = int(self.df.loc[(self.df["batter"] == player)  & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))].batsman_run.sum())
                balls=len(self.df.loc[(self.df['extra_type']!="wides")  & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs))  & (self.df["Season"].isin(Season)) & (self.df['extra_type']!="noballs") & (self.df['batter'] == player) ] )
                out = len(   self.df.loc[(self.df["player_out"] == player)  & (self.df["BowlingType"].isin(BowlingType)) & ~(self.df["dismissal_kind"].isin(dis))  & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
                boundary = len(self.df.loc[(self.df["batter"] == player) & ((self.df["batsman_run"] == 4) | (self.df["batsman_run"] == 6)  ) & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
                dots=len(self.df.loc[(self.df["batter"] == player)  & (self.df["Extras Run"]==0) & (self.df["batsman_run"]==0) & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs))  & (self.df["Season"].isin(Season))  ] )
    
    
    
    
                avg_run=run/out if out!=0 else np.inf
                bpercent=(boundary/balls)*100 if balls!=0 else 0
                strk_rate=(run * 100)/balls if balls!=0 else np.inf
                dpercent=(dots/balls)*100 if balls!=0 else 0
                
                df2 = {'player_name':player,'total_runs': int(run), 'outs':int(out),'balls_played': int(balls),'average_runs':avg_run,'strike_rate': strk_rate,'bpercent':bpercent,'dpercent':dpercent}
                if(balls>limit):
                        batsman_df =pd.concat([batsman_df ,pd.DataFrame(df2, index=[0])],ignore_index =True)
            return batsman_df.sort_values(by='strike_rate')
    
    
batcomp=Batter_comp(df)

with open('batting_comp.pkl', 'wb') as f:
    pickle.dump(batcomp, f)