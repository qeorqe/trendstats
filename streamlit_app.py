import streamlit as st
import pandas as pd
import clickhouse_connect
import plotly.express as px
import plotly.figure_factory as ff



# internal modules
import queries

try:
  client = clickhouse_connect.get_client(**st.secrets["clickhouse_cloud"], secure=True)
except:
  pass

@st.cache_resource(ttl=8600000)
def clickhouse_query(query):
  return client.query_df(query)


st.set_page_config(layout="wide")

st.title("trendstats")

st.write(
    "Various statistics about trends"
)

stats_by_year = clickhouse_query(queries.stats_by_year)
stats_by_year["year"] = stats_by_year["year"].apply(str)

col1, col2, col3 = st.columns(3, gap='medium')

with col1:
  total_channels = clickhouse_query(queries.total_channels)
  st.metric(label="Total channels", value=f"{total_channels['total'][0]:,}")

with col2:
  total_videos = stats_by_year["videos"].sum()
  st.metric(label="Total videos", value=f"{total_videos:,}")

with col3:
  total_views = stats_by_year["views"].sum()
  st.metric(label="Total views", value=f"{total_views:,}")


st.divider()

st.header("Youtube statistics by video publication year")

left, right = st.columns(2, gap='large')

with left:
  st.subheader("Videos")
  st.bar_chart(data=stats_by_year, x='year', y='videos',
              x_label='Year of video publication', 
              y_label='', 
              color='#f25e4e',
              horizontal=False, 
              stack=None, 
              width=None, 
              height=None, 
              use_container_width=True)

with right:
  st.subheader("Publishers (channels)")
  st.bar_chart(data=stats_by_year, x='year', y='uploaders',
              x_label='Year of video publication', 
              y_label='', 
              color='#f25e4e',
              horizontal=False, 
              stack=None, 
              width=None, 
              height=None, 
              use_container_width=True)


left, right = st.columns(2, gap='large')

with left:
  st.subheader("Views")
  st.area_chart(data=stats_by_year, x='year', y='views',
              x_label='Year of video publication', 
              y_label='', 
              color='#f25e4e',
              stack=None, 
              width=None, 
              height=None, 
              use_container_width=True)

with right:
  st.subheader("Likes")
  st.bar_chart(data=stats_by_year, x='year', y='likes',
              x_label='Year of video publication', 
              y_label='', 
              color='#f25e4e',
              stack=None, 
              width=None, 
              height=None, 
              use_container_width=True)


# tmp = pd.melt(stats_by_year, id_vars=['year'], 
#              value_vars=['viewes_per_video', 'likes_per_video', 'views_per_like', 'likes_per_dislike'])


col1, col2 = st.columns(2, gap="large")

with col1:
  st.line_chart(data=stats_by_year, 
                x='year', 
                y=['views_per_video', 'views_per_uploader'],
                x_label='Year', 
                y_label='Qty', 
                color=None,
                width=None, 
                height=None, 
                use_container_width=True)

with col2:
  st.line_chart(data=stats_by_year, 
                x='year', 
                y=['likes_per_video', 'views_per_like'],
                x_label='Year', 
                y_label='Qty', 
                color=None,
                width=None, 
                height=None, 
                use_container_width=True)

col1, col2 = st.columns(2, gap="large")

with col1:
  st.line_chart(data=stats_by_year, 
                x='year', 
                y='likes_per_dislike',
                x_label='Year', 
                y_label='Qty', 
                color=None,
                width=None, 
                height=None, 
                use_container_width=True)

with col2:
  st.line_chart(data=stats_by_year, 
                x='year', 
                y='videos_per_uploader',
                x_label='Year', 
                y_label='Qty', 
                color=None,
                width=None, 
                height=None, 
                use_container_width=True)


video_percentage_statistics = stats_by_year[["year"]]
video_percentage_statistics_columns = [
  "videos_with_ads",
  "videos_with_comments_enabled",
  "videos_with_subtitles",
  "videos_with_age_limit",
]

for col in video_percentage_statistics_columns:
  video_percentage_statistics[col] = 100.00 * stats_by_year[col] / stats_by_year["videos"]

# stats_by_year["share_of_views_of_videos_with_ads"] = stats_by_year["videos_with_ads"] / stats_by_year["videos"]


st.subheader("Video percentage statistics")
st.line_chart(data=video_percentage_statistics, 
              x='year', 
              y=video_percentage_statistics_columns,
              x_label='Year', 
              y_label='%', 
              color=None,
              width=None, 
              height=None, 
              use_container_width=True)


st.scatter_chart(data=stats_by_year, x='likes', y='dislikes',
              x_label='Year', 
              y_label='Video uploads', 
              color=None, 
              size='views',
              width=None, 
              height=None, 
              use_container_width=True)



stats_by_month = clickhouse_query(queries.stats_by_month)
# stats_by_month['month'] = stats_by_month['mm'].apply(lambda x: pd.Timestamp(f'1980-{x}').strftime("%B"))

months = [
    'Jan', 'Feb', 'Mar', 'Apr',
    'May', 'Jun', 'Jul', 'Aug',
    'Sep', 'Oct', 'Nov', 'Dec'
]

def plot_heatmap(df):
  fig = px.imshow(df,
                  x=df.columns,
                  y=df.index,
                  labels=dict(x="Year", y="", color=""),
                  color_continuous_scale='reds',
                )
  # Чтобы месяцы отображались в правильном порядке 
  fig.update_layout(
      yaxis=dict(
          tickvals=df.index,   # Позиции меток
          ticktext=months,     # Названия месяцев
      )
  )
  st.plotly_chart(fig, use_container_width=False, theme="streamlit") 

left, central, right = st.columns(3)

with left:
  plot_heatmap(stats_by_month.pivot(index='mm', columns='year')['views_per_uploader'].fillna(0))

with central:
  plot_heatmap(stats_by_month.pivot(index='mm', columns='year')['likes_per_video'].fillna(0))

with right:
  plot_heatmap(stats_by_month.pivot(index='mm', columns='year')['views_per_like'].fillna(0))


# Create distplot with custom bin_size
youtube_stats_subscribers = clickhouse_query(queries.youtube_stats_subscribers)


# Определяем категории
bins = [-1, 0, 1, 10, 100, 1e3, 5e3, 1e4, 1e5, 1e6]
labels = ["0", "0 to <1K", "1K to <10K", "10K to <100K", "100K to <1M", "1M to <5M", "5M to <10M", "10M to <100M", "100M to <1B"]

# Создаём новую колонку с категориями
youtube_stats_subscribers["subscribers"] = pd.cut(youtube_stats_subscribers["kilo_subscribers"], bins=bins, labels=labels, right=True).astype(str)

# Группируем и суммируем
result = youtube_stats_subscribers.groupby("subscribers", observed=True)["channels"].sum().reset_index()

st.subheader("Channels subscribers")
fig = px.bar(result, 
            x='subscribers', 
            y='channels',
            # labels={'subscribers':'Subscribers', 'channels':'Channels'}
            )
st.plotly_chart(fig)

# fig = px.bar(stats_by_year, 
# x="hour_of_day", y="count", color="event", 
# labels={
#     "hour_of_day": "Hour of Day", 
#     "count": "Event Count", 
#     "event": "Event Type"
# },
# color_discrete_map={"like": "light blue", "post": "red", "repost": "green"}
# )
# fig.update_layout(
#     legend=dict(
#         orientation="h",
#         yanchor="bottom",
#         y=1.1,
#         xanchor="center",
#         x=0.5
#     )
# )
# st.plotly_chart(fig)