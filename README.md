# Mental Health Subreddit Crawler

This repository contains a Python script that can crawl various mental health subreddits and extract submissions containing a specific keyword. This can be useful for analyzing trends in mental health discussions on Reddit, or for researching a specific topic within the mental health community.

## Usage

Before using this script, you'll need to set up a Reddit API account and add your API credentials to the `secrets.json` file.

```json
{
    "client_id": "your_client_id_here",
    "client_secret": "your_client_secret_here",
    "user_agent": "user_agent_to_use"
}
```

Once you have your API credentials set up, you can install the prerequisites listed in the `requirements.txt` file by running:



```bash
pip install -r requirements.txt
```


Once you have the prerequisites installed, you can run the script with the following command:

```bash
python main.py -query {query}
```

Replace `{query}` with the keyword you want to search for. For example, to search for submissions containing the term "ChatGPT", you would run:

```bash
python main.py -query chatgpt
```

The script will save the results to a CSV file named `{query}.csv`. For example, the results of the above search would be saved to `chatgpt.csv`.

## Example Result File

An example result file for a search of the term "ChatGPT" is provided in the file `chatgpt.csv`. This file contains a list of submissions from various mental health subreddits that contain the term "ChatGPT". The columns in the file include the subreddit name, submission title, submission text, and the URL of the submission.
