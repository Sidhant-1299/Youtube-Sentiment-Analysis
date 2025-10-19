// popup.js

document.addEventListener("DOMContentLoaded", async () => {
  const outputDiv = document.getElementById("output");
  const PROTOCOL = 'http';
  const PORT = '5555';
  const DOMAIN = 'localhost';
  const API_URL = `${PROTOCOL}://${DOMAIN}:${PORT}/`;

  // Get the current tab's URL
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const tab = tabs[0];
    const url = tab.url;
    const youtubeRegex = /^https:\/\/(?:www\.)?youtube\.com\/watch\?v=([\w-]{11})/;
    const match = url.match(youtubeRegex);

    if (!match || !match[1]) {
      outputDiv.innerHTML = "<p>This is not a valid YouTube URL.</p>";
      return;
    }

    const videoId = match[1];
    outputDiv.innerHTML = `<div class="section-title">YouTube Video ID</div><p>${videoId}</p><p>Fetching comments...</p>`;

    // Ask content script to scrape comments
    chrome.scripting.executeScript(
      {
        target: { tabId: tab.id },
        func: () => {
          // This runs inside the YouTube page
          const commentEls = document.querySelectorAll('#content-text');
          const comments = Array.from(commentEls).map(el => {
            const commentNode = el.closest('#comment');
            const authorNode = commentNode?.querySelector('#author-text');
            const timestampNode = commentNode?.querySelector('a[href*="lc"]'); // timestamp link
            return {
              text: el.innerText,
              authorId: authorNode?.innerText.trim() || 'Unknown',
              timestamp: timestampNode?.getAttribute('href') || ''
            };
          });
          return comments;
        }
      },
      async (results) => {
        const comments = results[0].result;
        if (!comments || comments.length === 0) {
          outputDiv.innerHTML += "<p>No comments found on this video.</p>";
          return;
        }

        outputDiv.innerHTML += `<p>Fetched ${comments.length} comments. Performing sentiment analysis...</p>`;
        const predictions = await getSentimentPredictions(comments);

        if (!predictions) return;

        const sentimentCounts = { "1": 0, "0": 0, "-1": 0 };
        const sentimentData = [];
        const totalSentimentScore = predictions.reduce((sum, item) => sum + parseInt(item.sentiment), 0);
        predictions.forEach((item) => {
          sentimentCounts[item.sentiment]++;
          sentimentData.push({ timestamp: item.timestamp, sentiment: parseInt(item.sentiment) });
        });

        const totalComments = comments.length;
        const uniqueCommenters = new Set(comments.map(c => c.authorId)).size;
        const totalWords = comments.reduce((sum, c) => sum + c.text.split(/\s+/).filter(w => w.length > 0).length, 0);
        const avgWordLength = (totalWords / totalComments).toFixed(2);
        const avgSentimentScore = (totalSentimentScore / totalComments).toFixed(2);
        const normalizedSentimentScore = (((parseFloat(avgSentimentScore) + 1) / 2) * 10).toFixed(2);

        outputDiv.innerHTML += `
          <div class="section">
            <div class="section-title">Comment Analysis Summary</div>
            <div class="metrics-container">
              <div class="metric"><div class="metric-title">Total Comments</div><div class="metric-value">${totalComments}</div></div>
              <div class="metric"><div class="metric-title">Unique Commenters</div><div class="metric-value">${uniqueCommenters}</div></div>
              <div class="metric"><div class="metric-title">Avg Comment Length</div><div class="metric-value">${avgWordLength} words</div></div>
              <div class="metric"><div class="metric-title">Avg Sentiment Score</div><div class="metric-value">${normalizedSentimentScore}/10</div></div>
            </div>
          </div>`;

        await fetchAndDisplayChart(sentimentCounts);
        await fetchAndDisplayTrendGraph(sentimentData);
        await fetchAndDisplayWordCloud(comments.map(c => c.text));

        outputDiv.innerHTML += `
          <div class="section">
            <div class="section-title">Top 25 Comments with Sentiments</div>
            <ul class="comment-list">
              ${predictions.slice(0, 25).map((item, i) => `
                <li class="comment-item">
                  <span>${i + 1}. ${item.comment}</span><br>
                  <span class="comment-sentiment">Sentiment: ${item.sentiment}</span>
                </li>`).join('')}
            </ul>
          </div>`;
      }
    );
  });

  async function getSentimentPredictions(comments) {
    try {
      const res = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ comments })
      });
      const result = await res.json();
      return res.ok ? result : null;
    } catch (e) {
      console.error("Error fetching sentiment predictions:", e);
      outputDiv.innerHTML += "<p>Error fetching sentiment predictions.</p>";
      return null;
    }
  }
});
