import requests
import json
import dotenv
import os
from datetime import timedelta, datetime


dotenv.load_dotenv(dotenv.find_dotenv())
bearer_token_tt = os.getenv("bearer_token_tt")

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
delta = timedelta(days=1)
start_time = f"{datetime.now().date()- delta}T00:00:00.00Z"
end_time = f"{datetime.now().date()}T00:00:00.00Z"

def auth() -> str:
    return bearer_token_tt

def create_url(start_time,end_time):
    query = "doutor estranho"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=author_id,conversation_id,created_at,text,public_metrics"
    filters = f"start_time={start_time}&end_time={end_time}"
    print(f"O dia de inicio das req é {start_time} e o final é {end_time}")
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(
        query, tweet_fields,filters
    )
    return url


def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def paginate(url, headers, next_token=""):
    if next_token:
        full_url = f"{url}&next_token={next_token}"
    else:
        full_url = url
    data = connect_to_endpoint(full_url, headers)
    yield data
    if "next_token" in data.get("meta", {}):
        yield from paginate(url, headers, data["meta"]["next_token"])

def main():
    bearer_token = auth()
    url = create_url(start_time, end_time)
    headers = create_headers(bearer_token)
    for json_response in paginate(url, headers):
        print(json.dumps(json_response, indent=10, sort_keys=True))


if __name__ == "__main__":
    main()