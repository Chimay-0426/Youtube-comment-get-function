# Youtube-comment-get-function
This repository contains a script to retrieve all comments from a YouTube video.

Context:

YouTube videos have two types of comments:

Parent Comments: These are the usual comments.
Child Comments: These are replies to the parent comments.
The number of comments displayed on a YouTube video includes both parent and child comments.

Files
get_comments.py: This Python script fetches all comments (both parent and child) from a YouTube video using its video ID. Instructions on how to use the script are provided within the code comments.

parent_comments_test.csv: This is an example output file of parent comments.

replied_comments_test.csv: This is an example output file of children_comments.


How to Get video ID

To get a video's ID from its URL, look for the v parameter. For example, in the URL [https://www.youtube.com/watch?v=YxFb6FNUJ6g], the video ID is the parameter of "v=hogehoge" and thus it is  YxFb6FNUJ6g.

The script can be modified to adjust the order of columns and include other items available in the YouTube Data API.

Data API refs is here [https://developers.google.com/youtube/v3/docs].

If you have any questions, please contact me at saepo12100426(at)gmail.com.

Thank you.

