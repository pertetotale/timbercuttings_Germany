# -*- coding: utf-8 -*-
import os    # echo %path% 
# os.add_dll_directory("C:\ProgramData\Anaconda3\condabin") # issue in Python > 3.8 with Windows, dll's are only loaded from trusted locations https://docs.python.org/3/whatsnew/3.8.html#ctypes This can be fixed by adding the dll path using os.add_dll_directory("PATH_TO_DLL")
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import pytz
#plt.style.use('seaborn-v0_8-ticks') 
# %config InlineBackend.figure_format = 'retina';
import altair as alt
from streamlit_theme_alt import streamlit_theme_alt
alt.themes.register("streamlit_alt", streamlit_theme_alt) #alt.themes.register("my_custom_theme", urban_theme) 
alt.themes.enable("streamlit_alt")
from typing import Dict, List, Tuple, Sequence

#import shapely
#import warnings
#from shapely.errors import ShapelyDeprecationWarning
#warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning) 

st.set_page_config(layout="wide", page_title="Forest tree loss due to damage in Germany by various kinds of damage", page_icon ="🧊", menu_items={
        'About': "#### Overview of various kinds of damage to cause forest tree losses in Germany. Insects have become a huge contributor to timber losses over the last years. \
        More info: Statistisches Bundesamt (Destatis), https://www.destatis.de/EN/Themes/Economic-Sectors-Enterprises/Agriculture-Forestry-Fisheries/Forestry-Wood/, http://umwelt.nrw.de, http://www.waldinfo.nrw.de/"
    })
st.subheader('Forced timbercutting in Germany grouped by cause of damage and year')
st.markdown("Germany has forests which cover about one third of its area. In recent years however, the group of the needle-leaved trees has been hit hard by insect damage, esp. the Norway spruces. ")
st.markdown("The European spruce bark beetle, Ips typographus, is the main culprit for the damage. Their larvea bore tunnels under the bark of needle-leaved trees. \n \
    These beetles thrive in a warm climate with little to moderate rainfall. Beetle population growth is promoted by increasing temperatures that reduce developmental time, allowing for the production of additional generations per year. In these conditions the beetles can swarm 3 of 4 times each year. \
        After some time the infested tree's canopy dries up, often starting at the top. The timber of infested trees is not marketable due to the appearance of those typical markings, which are undesired by customers. ")
st.markdown("Also, most needle-leaved trees in Germany don't grow on compatible soils, nor stand at elevations that provide optimal growth conditions. Furthermore, the resistance of conifer trees to beetle attack is compromised during heat and drought stress. \
So, these coniferous trees have been weakened by these poor conditions, which slow down their natural defense against invading insects. \
    Hence we notice more forced timbercuttings in Central Germany the year(s) after a dry season.")

States: List[str] =['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen','Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
           'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen','Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen'] # so without! Total
cities: List[str]= ['Berlin', 'Bremen','Hamburg']
Causes: List[str] =['Insects', "Wind/Storm", "Snow/Ice", "Drought",'Total']  #"unknown",
Tree_types: List[str] =['Oak and red oak', 'Beech and other deciduous wood','Pine and larch', 'Spruce, fir,Douglas fir and other coniferous trees','Total']
totalcolorrange: List[str] =["sandybrown", "silver", "olivedrab", "slateblue", "black"] 
Tree_domain: List[str] =['Oak and red oak', 'Beech and other deciduous wood','Pine and larch', 'Spruce, fir,Douglas fir and other coniferous trees'] # so without Total
colorrange: List[str] =["sandybrown", "silver", "olivedrab", "slateblue"]     # so without Total

tab1,tab2,tab3, tab4,tab5 = st.tabs( ["**Forced timbercuttings in Germany by cause of damage**", "**Number of timbercuttings by tree type and by federal state**", "**Insect caused damage**","**Forested area lost 2019-2021**",
                "**Marketability of timber: standing vs. felled**"])

Timbercut_causeB = pd.read_csv(r"41261-0012Schadholzeinschlag_Bundesländer_Einschlagsursache.csv", sep=";",skiprows=6, engine="python", encoding="cp1252", skipfooter=4, decimal=",")# , nrows=nrows
Timbercut_causeB=Timbercut_causeB[Timbercut_causeB.Owner=="Insgesamt"]  # no Privat data etc. needed
Timbercut_causeB=Timbercut_causeB.drop(columns= "Owner", axis=1)
st.dataframe( Timbercut_causeB, width=1600,)

#Timbercut_causeB["value"] =Timbercut_causeB["value"].astype( "float32") 
Timbercut_causeB =Timbercut_causeB.replace("-","0")  # fillna( 0)   # , na_values="-"
lossyears: List[int]= [2015,2016,2017,2018,2019,2020,2021]

Timbercut_causeB["Year"]= Timbercut_causeB.loc[:,"Year"].astype( "int16")
Timbercut_causeB2018All= Timbercut_causeB[Timbercut_causeB.Year.isin(lossyears )]   #.copy()
#Timbercut_causeB2018All.sample(10)

treetypedict: Dict[str, str]= {"Fichte, Tanne, Douglasie und sonstiges Nadelholz":'Spruce, fir,Douglas fir and other coniferous trees', "Kiefer und Lärche":'Pine and larch',
    "Buche und sonstiges Laubholz":"Beech and other deciduous wood", "Eiche und Roteiche":"Oak and red oak","Insgesamt":"Total", "Insekten":"Insects",
    "Trockenheit":"Drought", "Schnee/Duft":"Snow/Ice","Wind/Sturm":"Wind/Storm","Sonstiges":"Other"}
Timbercut_causeB2018All["Cause"]= Timbercut_causeB2018All["Cause"].map( treetypedict )
Timbercut_causeB2018All["Tree_type"] = Timbercut_causeB2018All["Tree_type"].map( treetypedict)
print( "Timbercut_causeB2018All", Timbercut_causeB2018All )

df =Timbercut_causeB2018All.copy()
df= df.melt(id_vars=["Year","Cause","Tree_type"], var_name="German State")  # ,"Owner"
df['Year'] =pd.to_datetime( df.Year, format='%Y' ) # .astype('datetime64["Y"]')  np.datetime64(1, 'Y')
df = df.rename( columns={"value": "Value"}, errors="raise" )            # avoid strange behavior
df['Cause'] = df.Cause.replace( np.nan, "unknown") 

print("df.head():", df.head() )    # info= None

@st.cache( allow_output_mutation=True)
def load_data( df):
    # df['date'] = df.Year.astype('datetime64["Y"]')
    data= df  #.drop(columns="Owner", axis=1)
    return data

#if st.checkbox('Show raw data'):
#    st.subheader('Raw data')
#    st.write(data)

# dfB = df[ (df["Tree_type"]== select_tree.value)& (df["Cause"]== select_cause.value) ] # (df["German State"]== select_state.value)
# dfB = dfB.set_index("Year")
# dfB"

# Pick German State / cause of damage / Tree_type
state_filter = st.sidebar.selectbox('Pick **Federal State**', States , index=10)  # 10= RLP
cause_filter = st.sidebar.radio('Pick **Cause of damage**', Causes )
Tree_filter = st.sidebar.radio('Pick **Tree type**', Tree_types, index=4 )
agree = st.sidebar.checkbox('Show **Extra data**', value=False, key="extra_dataframes" )

if agree: 
    data_load_state = st.text('Loading data...')
    #data = load_data( df)   #
    data_load_state.text("Done!  (using st.cache)")
data = load_data( df)
filtered_data = data[data["German State"] == state_filter]

with tab1:
    st.subheader('Number of tree cuttings grouped by federal state since 2015')
    st.success('Hint: select the values for Federal State, the cause of damage and the tree type in the side bar. ' )

    dfB = data[ (data["Tree_type"]== Tree_filter)& (data["Cause"]== cause_filter ) & (data["German State"]== state_filter )]
    st.dataframe( dfB, width=1600, )
    dfB.Value =dfB.Value.astype( "float32")   #is_numeric()   # infer_objects()
    #dfB = dfB.loc[:, ["Year","Value"]]     # used for the .area_chart
    dfB["Year"]= dfB.Year.dt.year  #dfB = dfB.set_index("Year")
    print("dfB.info", dfB.info(verbose=True) )
    #st.write( info)

    if agree: st.write(dfB)  # extra df's / data when checked
    #st.area_chart(dfB, x="Year", y="Value", use_container_width=True, )
    alt_lines =alt.Chart(dfB).mark_line().encode(
        x='Year:O',
        y=alt.Y( 'Value', type='quantitative', ),  #'sum(Value:Q)'  scale=alt.Scale(type="symlog")
        color=alt.Color('Tree_type:N', scale=alt.Scale(domain=Tree_types, range=totalcolorrange)), 
        #row='Tree_type:N',
        strokeDash='German State:N'#, sort=["Baden-Württemberg","Bayern","Brandenburg","Hessen","Mecklenburg-Vorpommern","Niedersachsen","Nordrhein-Westfalen", "Rheinland-Pfalz","Saarland","Sachsen","Sachsen-Anhalt", "Schleswig-Holstein","Thüringen"])
        ).properties( width=1600,)
    st.altair_chart(alt_lines , ) # my theme or theme="streamlit"

    st.info('Note: The values for the causes of damage are the totals of the logged timber in 1000 m³.' )


fig, ax = plt.subplots(1,1, )
df2 =data[ (data["Tree_type"]== "Total")& (data["Cause"]== "Total" )]  # ["German State","Value"]
df2.Value =df2.Value.astype( "float32") 
df2 =df2.loc[:, ["Year","German State","Value"]]
#df2 = df2.set_index(["Year","German State"]) # 
#df2 = df2.sort_index() 
#st.dataframe(df2, width=1600, )


import plotly.express as px     # Timbercut_landerR

Timbercut_lander= pd.read_excel("Excess Green index etc.xlsx", index_col=0,# owv doubles in German state
                                sheet_name="timbercuttingbylander2", engine='openpyxl',verbose=1,skiprows=1 ) #na_values="",
#      Timbercut_lander= pd.read_excel( r"C:\Users\*\Documents\Notebooks\streamlit\41261-0010_Holzeinschlag Bundesländer, Jahre, Holzartengruppen.xlsx", sheet_name="41261-0010", engine='openpyxl',verbose=1,skiprows=4,skipfooter=36, na_values="-", index_col=[0,1]); #
Timbercut_lander= Timbercut_lander.dropna()
if agree: st.dataframe(Timbercut_lander )
Timbercut_lander.Year= pd.to_datetime( Timbercut_lander.Year,format="%Y", errors="ignore") # yearfirst=True,Year
#Timbercut_lander = Timbercut_lander.tz_localize(pytz.timezone('Europe/Brussels'))
#Timbercut_lander["Year"]= Timbercut_lander["Year"].dt.tz_convert("UTC")
       # excluding the cities
Timbercut_lander= Timbercut_lander[~ Timbercut_lander["German State"].isin( cities)  ]
Timbercut_landerR= Timbercut_lander.reset_index()

with tab2:
    st.subheader('Number of timbercuttings by tree type and by federal state')

    if agree: st.dataframe( Timbercut_landerR, width=1600, height=600)

    fig = px.bar(Timbercut_landerR, x=Timbercut_landerR.Year.dt.year,  y=["Oak", "Beech and other deciduous woods","Pine and larch", "Spruce, fir,douglas fir and other coniferous wood"],  #
                #y= Timbercut_landerR["German State"],
                title="Timbercutting Tree Species vs. German State", facet_col="German State",
                labels={"value": "1000 m³", "variable": "Tree species"}, barmode='group', log_y=True, 
                color_discrete_map={"Oak": "sandybrown", "Beech and other deciduous woods": "silver", "Pine and larch":"olivedrab", "Spruce, fir,douglas fir and other coniferous wood":"slateblue"},
                template="simple_white"
                )
    fig.update_layout(font_family="Rockwell", showlegend=True)
    fig.update_traces(textfont_size=11, textangle=0, textposition="outside", cliponaxis=False)
    #fig.show()
    st.plotly_chart(fig, use_container_width=True,)


# Using no longer Timbercut_landerR, but df for insect damage 
df.Value =df.Value.astype( "float32") 
df= df[df["Cause"] == "Insects"]
df= df[df["Tree_type"] != "Total"]
if agree: st.dataframe( df) 

dfX= df[df["Tree_type"] != "Total"]
#dfX= df.drop( columns=["Owner"],axis=1);
cities= ['Berlin', 'Bremen','Hamburg'] # 
#dfX= df[~ df["German State"].isin( cities)  ]
print("dfX.info():", dfX.info())
lossyears2= [2017,2018,2019,2020,2021]
#dfX= dfX[ dfX["Year"].isin( lossyears2) ]
dfX1 =dfX.copy()
print("dfX1.info():", dfX1.info(verbose=True))
#dfX1.Year =dfX1.Year.astype( "category") 

if agree: st.write(dfX1.head(1))
# .dt.year sample(12)
dfX2= dfX1.drop( columns="Cause", axis=1)  #  # exclusion of cause
#dfX = dfX.tz_localize(pytz.timezone('US/Eastern'))
#dfX["Year"]= dfX["Year"].dt.tz_convert("UTC")
print("dfX2.info():", dfX2.info(verbose=True)) #st.write(dfX2.info())
if agree: st.dataframe( dfX2, width=1600, ) # print(dfX.info()() )

# fig = px.bar(dfX2, x="Tree_type",  # y=dfX["Tree_type"] ,["Oak", "Beech and other deciduous woods","Pine and larch","Spruce, fir,douglas fir and other coniferous wood"] .dt.year
#         facet_col= "German State", # Timbercut_landerR.Year.dt.year
#     title="Timbercutting Tree Species", 
#     facet_row=dfX2.Year.dt.year , # .dt.year
#     color="Tree_type", # Year    dfX.Year.dt.year
#      labels={"value": "1000 m³", "variable": "Species"},  log_y=True, barmode='group',
#      color_discrete_map={"Oak": "sandybrown", "Beech and other deciduous woods": "silver", "Pine and larch":"olivedrab","Spruce, fir,douglas fir and other coniferous wood":"slateblue"},
#         template="seaborn", height=2990, width=1700,   # simple_white
#     category_orders={"Tree Species": ["Oak", "Beech and other deciduous woods","Pine and larch","Spruce, fir,douglas fir and other coniferous wood"],
#         "German State": ['Baden-Württemberg','Bayern','Hessen','Mecklenburg-Vorpommern', 'Niedersachsen','Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen','Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen'],
#           }   #"Year":[2018,2019,2020] 'Berlin','Bremen','Hamburg',
#             )

with tab3:
    from PIL import Image
    imageIps = Image.open("figs/Fig.The Eurasian spruce bark beetle.webp")

    # Altair chart
    st.subheader( "Insect caused damage")
    st.image( imageIps, caption="Adult Ips typographus (a) front and (b) side view with sensory array on antennae indicated (yellow arrows). c Pupae in bark. d Damage on Norway spruce (Picea abies) at tree level (with one of several hundred galleries indicated with white arrows; MG = straight egg tunnel made by one mother and LG = winding larval tunnels), e Damage at landscape level of mixed forest with Norway spruce (all brown), while trees with green crowns are Scots pine (Pinus sylvestris) or deciduous trees. Pictures (a, b, d) from Belgium by Gilles San Martin (URL: https://flickr.com/people/sanmartin/), under CC BY-SA 2.0, (c) by blickwinkel, Alamy Stock Photo (licenced), and (e) from Czech Republic, Central Bohemia, Koberovice, August 2019 by Jan Liška. (source: https://www.nature.com/articles/s42003-021-02602-3/figures/1)",
            width=1500)

    st.dataframe( dfX2, width=1600, )  # dfx1: cause is all instects, so must go: dfX2
    #dfX2 =dfX2[ (dfX2["Tree_type"]!= "Total")& (dfX2["Cause"]!= "Total" )] # the Totals must go for this plot
    dfX2["Year_only"]= dfX2.Year.dt.year
    #dfX2["Value"]=dfX2["Value"]+0.00000001    # avoid errors from 0 when using log scale
    dfX2 =dfX2.sort_values( ["Year_only",'German State',"Tree_type"])
    print("dfX2.head()", dfX2.head(20), "dfX2.tail()", dfX2.tail(10))
    print("dfX2.info():", dfX2.info(verbose=True))
    dfX22= dfX2[dfX2["German State"].isin(["Baden-Württemberg","Bayern","Brandenburg","Hessen","Mecklenburg-Vorpommern","Niedersachsen","Nordrhein-Westfalen", "Rheinland-Pfalz","Saarland","Sachsen","Sachsen-Anhalt", "Schleswig-Holstein","Thüringen"])]

    alt_bars =alt.Chart(dfX22 ).mark_bar().encode(
        y='Year_only:O',
        x=alt.X( ('Value'), type='quantitative', ),  #'sum(Value:Q)'  scale=alt.Scale(type="symlog")
        color=alt.Color('Tree_type:N', scale=alt.Scale(domain=Tree_domain, range=colorrange)), 
        #row='Tree_type:N',
        column=alt.Column('German State:N', sort=["Baden-Württemberg","Bayern","Brandenburg","Hessen","Mecklenburg-Vorpommern","Niedersachsen","Nordrhein-Westfalen", "Rheinland-Pfalz","Saarland","Sachsen","Sachsen-Anhalt", "Schleswig-Holstein","Thüringen"])
        ).properties( width=160, height=260)
    st.altair_chart( alt_bars, ) #use_container_width=True,

    #2019 to 2021 timber losses due to insects
    image19 = Image.open("figs/2019 losses to insects.png")
    image20192020 = Image.open("figs/percentage of timbercuttings due to insect damage vs. the regional forested area.jpg")
    image21 = Image.open("figs/2019, 2020 and 2021 summed losses to insects.png")
    st.markdown("#### Timber losses due to insects: in 2019, the years 2019 and 2020 summed, and for the period 2019-2021 summed", )
    losscol3, losscol4, losscol5= st.columns(3, )
    with losscol3: st.image(image19, caption="Timber losses due to insects in the year 2019  [1000 m³ excluding bark]", width=550, )
    with losscol4: st.image(image20192020, caption="The percentage of timbercuttings due to insect damage vs. the regional forested area in the years 2019 and 2020 summed", width=650, )
    with losscol5: st.image(image21, caption="Sum of timber losses due to insects in the years 2019, 2020 and 2021  [1000 m³ excluding bark]", width=550, )

# streamlit run c:/Users/VanOp/Documents/Notebooks/streamlit/create-kever-app.py

#fig2, ax2 = plt.subplots()
#ax2.bar([dfX2["German State"].values,dfX2["Tree_type"].values],  height="Value") # bins=20
#st.pyplot(fig2, ) #use_container_width=False
# active=""
# fig = px.histogram(Timbercut_landerR, x="German State",  y=["Oak", "Beech and other deciduous woods","Pine and larch","Spruce, fir,douglas fir and other coniferous wood"],  # .dt.year
#         #y= Timbercut_landerR["German State"],  Timbercut_landerR.Year.dt.year
#     title="Timbercutting Tree Species", facet_row=Timbercut_landerR.Year.dt.year, # color="Tree Species", # Year
#      labels={"value": "1000 m³", "variable": "Species"}, barmode='group', log_y=True,
#      color_discrete_map={"Oak": "sandybrown", "Beech and other deciduous woods": "silver", "Pine and larch":"darkolivegreen","Spruce, fir,douglas fir and other coniferous wood":"slateblue"},
#         template="simple_white", height=1100, width=1600,
#     category_orders={"Tree Species": ["Oak", "Beech and other deciduous woods","Pine and larch","Spruce, fir,douglas fir and other coniferous wood"],
#         "German State": ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen','Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen','Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen','Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen'],
#          "Year":[2018,2019,2020] }
#             )
# fig.update_layout(font_family="Rockwell", showlegend=True)
# fig.update_traces(textfont_size=11, textangle=0, textposition="outside", cliponaxis=False)
# #fig.show()
# st.plotly_chart(fig, use_container_width=False,)

    st.markdown( "#### Average temperature - Average precipitation")
    weatherdata=[[2011,0.6316,2.6607,1.996,1.1942,9.6,718],[2012,0.8353,0.7437,2.4414,0.8696,9.1,768],[2013,0.8702,1.1641,2.284,1.7041,8.7,781],[2014,0.8845,0.2301,2.5905,1.7523,10.3,729],
    [2015,0.8701,0.3117,8.3499,3.3483,9.9,688],[2016,1.1929,0.0968,1.8224,4.6678,9.6,736],[2017,1.531,0.0758,4.6544,6.0032,9.6,850],[2018,1.96386270025083,0.148986665595884,18.4968855580444,11.3239896728837,10.4,590],
    [2019,5.4917,2.4652,6.5821,31.7024,10.2,730],[2020,6.4026,0.2658,10.1638,43.2953,10.4,710],[2021,6.2773,0.8066,2.3249,41.0814,9.2,805]]

    Timbercutting_weather: pd.DataFrame = pd.DataFrame( columns=["Year","Other causes","Snow/rime","Wind/storm","Insects", "Average temperature", "Average precipitation"], data=weatherdata )
    Timbercutting_weather= Timbercutting_weather.set_index( "Year")
    #print(Timbercutting_weather )
    meteocol1, meteocol2= st.columns( 2)
    with meteocol1: 
        st.line_chart(Timbercutting_weather[["Average temperature"]], width=450 )
    with meteocol2:
        st.line_chart(Timbercutting_weather[["Average precipitation"]], width=450 )

with tab4:
    st.subheader("Forest area lost in the period 2019-2021") 
    st.markdown("The relation between forested area in hectares, *Waldfläche in 2016*, and the amount of timber in m³, was made by calculating a value for the national wooddensity using the total value of Germany's standing forest in m³. ")
    woodedarea_lander= pd.read_excel("Excess Green index etc.xlsx", index_col=0,  # =bundesland / German state
                                sheet_name="woodedarea", engine='openpyxl',na_values="",verbose=1,skiprows=5, skipfooter=1 ) 
    print(woodedarea_lander.columns)

    st.markdown("#### Summed losses for all damages in 2019 and 2020 " ) #  ? due to insects 
    Kuub= pd.read_csv(r"Wood_lost_2019_2020_m3.csv", sep=",", encoding="UTF-8", engine="python",decimal=".", index_col=0) #UTF-8
    st.dataframe(Kuub.style.background_gradient(axis=0, cmap="YlOrRd", subset="PCT") , width=1150,)

    import geopandas as gpd    #Bundeslandergrenzen_2014_mit_Einwohnerzahl_shp\Bundesländer_2014_ew.shp
    bundeslander= gpd.read_file(r"tufts-germany-states-15-shapefile.zip", lw=0.25,  )
    bundeslander.crs="EPSG:4326"   #st.write("bundeslander.crs", bundeslander.crs)          #GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",
    ax = bundeslander.plot(column="StateName1",legend=True, categorical=True,figsize=(7,7), legend_kwds={'loc':'center left','bbox_to_anchor':(0.95,0.5),}, cmap="tab20b") #,figsize=(7, 6)
    ax.set_axis_off()

    # merge woodedarea_lander + bundeslander
    woodedarea_landerMerge =pd.merge(bundeslander, woodedarea_lander, left_on="StateName1", right_index=True )
    woodedarea_landerMerge.crs="EPSG:4326"
    print(woodedarea_landerMerge[["StateName1", "Waldfläche2020","Forest_PCT2020"]].sample(8) )
    #st.dataframe(woodedarea_landerMerge[["StateName1", "Waldfläche2020","Forest_PCT2020"]].sample(8) )  #

    st.markdown("#### Percentage of forested area by State", )
    woodedarea_plot= woodedarea_landerMerge.plot(column='Forest_PCT2020',scheme='equal_interval',k=9, cmap='YlGn', legend=True,lw=0.5,figsize=(6,6),legend_kwds={'loc':'center left','bbox_to_anchor':(0.95,0.5),'fmt':"{:.1f}", }); 
    woodedarea_plot.set_axis_off() # Forest_area_PCT_diff = difference betw 2020 and end 2021/2022
        
    Forest_area_PCT_diff_plot =woodedarea_landerMerge.iloc[[0,1,4,5,6,7,8,9,10,11,12,13,14,15],:].plot(column='Forest_area_PCT_diff',scheme='equal_interval',k=9,cmap='RdYlGn',legend=True,lw=0.5,figsize=(6,6),legend_kwds={'loc':'center left','bbox_to_anchor':(0.95,0.5),'fmt':"{:.1f}", });
    Forest_area_PCT_diff_plot.set_axis_off()  #vmin=-5.9,vmax=3,
    st.markdown("The 3rd map shows the difference in percentages of forest area gained or lost between 2020 and the end of 2021/2022. This is conform the notion that the spruce beetles are moving to more Northern located habitats.") 
    st.markdown("Note that the % for Berlin and Brandenburg were not used, as it seems a transfer of 17000 ha. forest area from Brandenburg to Berlin occured.")
    

    losscol1, losscol2, losscol2b= st.columns(3, )
    with losscol1: st.pyplot( ax.figure ) 
    with losscol2: st.pyplot( woodedarea_plot.figure )
    with losscol2b: st.pyplot( Forest_area_PCT_diff_plot.figure )
  
    # Timbercut_causeB2018All_statecoordin= pd.read_excel(r"C:\Users\*\Documents\Notebooks\streamlit\Timbercut_causeB2018All_statecoordin.xlsx")  # this makes just circle markers...
    # st.dataframe(Timbercut_causeB2018All_statecoordin, )
    # gdf = gpd.GeoDataFrame( Timbercut_causeB2018All_statecoordin,geometry=gpd.points_from_xy(Timbercut_causeB2018All_statecoordin.Longitude, Timbercut_causeB2018All_statecoordin.Latitude) )#geometry=gpd.points_from_xy(Timbercut_causeB2018All_statecoordin.Longitude, Timbercut_causeB2018All_statecoordin.Latitude)
    # st.write("gdf.crs", gdf.crs)
    # gdf.crs= "EPSG:4326"     # gdf.crs      # #gdf
    
    # gdf[(gdf.Year==2020)&(gdf.Cause=="Insects")&(gdf.Tree_type=="Total")]
    # #st.write( gdf[(gdf.Year==2020)&(gdf.Cause=="Insects")&(gdf.Tree_type=="Total")])  #.head())
    # #world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    # #ax = world[world.continent == 'South America'].plot(        color='white', edgecolor='black')
    # gdf_fig= gdf.plot(ax=ax, column= "value", cmap="autumn", ) # color='red'  colorbar=True
    
    # st.pyplot(gdf_fig.figure )
with tab5:
    st.subheader("**Marketable timber: standing or felled**") 
    st.markdown("Merchantable Timber means standing trees by species and product which are because of size and quality, salable within a reasonable time period from the subject lands.")
    st.markdown("The Timber in this case has already been felled. More than 2/3 of wood damaged by insects fails to get good price offerings. As a result, much of this timber might end up as wood chips for power production.")
    st.image(["./figs/Timbercutting_cause_and_tree_species_95_0.png"] ,width=700, caption=["More than 2/3 of wood damaged by insects fails to get good price offerings"], output_format="png")
    st.image(["./figs/Timbercutting_cause_and_tree_species_103_0.png"] ,width=1500, caption=["Damaged timber by insects vs. the total timber loss by any cause of damage"], output_format="png")

#   cd C:\Users\*\Documents\Notebooks\streamlit   streamlit run create-kever-app.py --global.dataFrameSerialization="legacy"
# st.map(filtered_data)                                                    https://developer.mozilla.org/en-US/docs/Web/CSS/color_value
# startdate and enddate must follow Timestamp type
# starttime and endtime must follow datetime.time type

# cd c:/Users/*/Documents/Notebooks/streamlit/
# python -m streamlit run c:/Users/*/Documents/Notebooks/streamlit/create-kever-app.py

# create a new repository on the command line

# echo "# timbercuttings_Germany" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/pertetotale/timbercuttings_Germany.git
# git push -u origin main
