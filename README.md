# Youtube-comment-get-function
This is a repository to explain a code which is able to get all comments attached to a youtube video.

First, let me  make it clear regarding the context of Youtube video. There two types of comments for a video, ususal comments(from here, I'll call parent comment) and replied comments for some usual comments(here, I'll call children comment) . In the UI of a youtube video, the number of comments is displayed. Such number include both.

 ・get_comments.py is sublime lines of python to get all comments of a video, whose number is equal to the number displayed in the UI of a video, with a video ID. How-to is indicated inside the comments-out of the code.

・You can know a video id from the URL of a video.For exmample, regarding [https://www.youtube.com/watch?v=YxFb6FNUJ6g], the ID is the parameter is "v=hogehogehoge"　and it is YxFb6FNUJ6g. 

・test_comments.csv is the output example. 

Conerning the order of columns, other items available in the YOutube data API, and etc, you can arrange the code.

If you have some questions, please contact me to this address. saepo12100426(at)gmail.com

Thank you.

