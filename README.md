# Youtube-Sentiment-Analysis

A Chrome Extension powered by a Dockerized Flask backend and a LightGBM model that performs real-time sentiment analysis on YouTube comments.
The extension fetches visible comments, sends them to the backend API for prediction, and displays an interactive pie chart and sentiment score directly on the YouTube page.

## Usage

#### Flask Server API

** To build the docker image **
```
git clone https://github.com/Sidhant-1299/Youtube-Sentiment-Analysis/
cd Youtube-Sentiment-Analysis
docker build -t yt-sentiment-analysis
docker run -p 5555:5555 yt-sentiment-analysis
```

#### For fronted chrome extension

1. Go to chrome:://extenstions
2. Turn on Developer mode
3. Find Youtube-Sentiment-Analysis/yt-chrome-plugin-frontend and load it as extension



## Tutorial 
https://github.com/user-attachments/assets/cbcc8904-4069-4d1b-8a80-892778fb189f


## License
This project is open-sourced under the MIT License