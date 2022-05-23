# Vietnamese Text Highlighter (Summarization)

A tool to extract important sentences in Vietnamese text. (Extraction-based summarization)

Demo: https://nhattestnet.pythonanywhere.com/vn-text-highlighter


## API

`https://nhattestnet.pythonanywhere.com/vn-text-highlighter/api/v1/?num=&text=`

- `num`: Number of sentences in the summary.
- `text`: The raw text you want to summarize.

Returned data:

`{
"summary": "Here's your summary."
}`
