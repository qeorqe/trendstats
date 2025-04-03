
table_youtube = "youtube_optimized"

total_channels = f"""
    SELECT uniqCombined(uploader_id_half_md5) AS total
    FROM {table_youtube}
"""

total_videos = f"""
    SELECT count(1) AS total
    FROM {table_youtube}
"""

stats_by_year = f"""
    SELECT YEAR(upload_date) year
    , count(*) videos
    , uniq(uploader_id_half_md5) uploaders
    , sum(view_count) views
    , sum(like_count) likes
    , sum(dislike_count) dislikes
    , sum(is_ads_enabled) videos_with_ads
    , round(views/videos, 2) views_per_video
    , round(likes/videos, 2) likes_per_video
    , round(views/uploaders, 2) views_per_uploader
    , round(videos/uploaders, 2) videos_per_uploader
    , round(views/likes, 2) views_per_like
    , round(likes/dislikes, 2) likes_per_dislike
    , sum(is_crawlable) videos_are_crawlable
    , sum(is_comments_enabled) videos_with_comments_enabled
    , sum(has_subtitles) videos_with_subtitles
    , sum(is_age_limit) videos_with_age_limit
    FROM {table_youtube}
    WHERE YEAR(upload_date) BETWEEN 2000 and 2021
    GROUP BY 1
"""

stats_by_month = f"""
    SELECT YEAR(upload_date) year
    , formatDateTime(upload_date, '%m') mm
    , count(*) videos
    , uniq(uploader_id_half_md5) uploaders
    , sum(view_count) views
    , sum(like_count) likes
    , sum(dislike_count) dislikes
    , sum(is_ads_enabled) videos_with_ads
    , round(views/videos, 2) views_per_video
    , round(likes/videos, 2) likes_per_video
    , round(views/uploaders, 2) views_per_uploader
    , round(videos/uploaders, 2) videos_per_uploader
    , round(views/likes, 2) views_per_like
    , round(likes/dislikes, 2) likes_per_dislike
    FROM {table_youtube}
    WHERE YEAR(upload_date) BETWEEN 2000 and 2021
    GROUP BY 1,2
"""


##### Распределение каналов по килоподписчикам

# CREATE TABLE IF NOT EXISTS dma.youtube_stats_subscribers
# (
#     `kilo_subscribers` INTEGER PRIMARY KEY,
#     `channels` INTEGER NOT NULL 
# )
# ENGINE = MergeTree 
# ORDER BY kilo_subscribers;
# SELECT * FROM dma.youtube_stats_subscribers;
# INSERT INTO dma.youtube_stats_subscribers 
# WITH stats AS (
#     SELECT
#         uploader_id_half_md5 AS channel,
#         ceiling(max(uploader_sub_count)/1000) AS kilo_subscribers
#     FROM youtube
#     GROUP BY 1
#     SETTINGS max_bytes_before_external_group_by = 2e9
# )
# SELECT kilo_subscribers, count(*) channels
# FROM stats
# GROUP BY 1
# ORDER BY 1;

youtube_stats_subscribers = f"""
    SELECT * FROM dma.youtube_stats_subscribers
"""