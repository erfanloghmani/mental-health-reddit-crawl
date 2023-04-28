import json
import pandas as pd

import praw
import prawcore
import argparse

secrets = json.load(open("secrets.json"))

reddit = praw.Reddit(
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    user_agent=secrets["user_agent"],
)

# Mental Health Subreddits from Sharma, Choudhary
mental_subs = [
    "abuse",
    "adultsurvivors",
    "afterthesilence",
    "Anger",
    "bullying",
    "CPTSD",
    "domesticviolence",
    "emotionalabuse",
    "ptsd",
    "PTSDCombat",
    "rapecounseling",
    "StopSelfHarm",
    "survivorsofabuse",
    "SurvivorsUnited",
    "traumatoolbox",
    "Agoraphobia",
    "Anxiety",
    "BipolarReddit",
    "BipolarSOs",
    "BPD",
    "dpdr",
    "psychoticreddit",
    "MaladaptiveDreaming",
    "Psychosis",
    # "PanicParty", # Was not found
    "schizophrenia",
    "socialanxiety",
    "calmhands",
    "CompulsiveSkinPicking",
    "OCD",
    "Trichsters",
    "7CupsofTea",
    # "BackOnYourFeet", # Was not found
    "Existential_crisis",
    "getting_over_it",
    "GriefSupport",
    "helpmecope",
    "hardshipmates",
    # "HereToHelp", # Was not found
    "itgetsbetter",
    "LostALovedOne",
    "offmychest",
    "MMFB",
    "Miscarriage",
    "reasonstolive",
    "SuicideBereavement",
    "therapy",
    "depression",
    "depressed",
    "ForeverAlone",
    "GFD",
    "lonely",
    "lonelywomen",
    "mentalhealth",
    "Radical_Mental_Health",
    "SuicideWatch",
]
# These subreddits had name changes
mental_subs[0] = "NarcissisticAbuse"
mental_subs[12] = "AbuseInterrupted"
mental_subs[43] = "Therapylessons"

# Subgroups
trauma = mental_subs[:15]
psychosis = mental_subs[15:26]
compulsive = mental_subs[26:30]
coping = mental_subs[30:44]
mood = mental_subs[44:]

fields_obj = [
    "author",
    "comments",
    "poll_data",
    "subreddit",
]
fields_nobj = [
    "author_flair_text",
    "clicked",
    "created_utc",
    "distinguished",
    "edited",
    "id",
    "is_original_content",
    "is_self",
    "link_flair_template_id",
    "link_flair_text",
    "locked",
    "name",
    "num_comments",
    "over_18",
    "permalink",
    "saved",
    "score",
    "selftext",
    "spoiler",
    "stickied",
    "title",
    "upvote_ratio",
    "url",
]
user_fields = [
    "comment_karma",
    "created_utc",
    "has_verified_email",
    "icon_img",
    "id",
    "is_employee",
    "is_friend",
    "is_mod",
    "is_gold",
    "is_suspended",
    "link_karma",
    "name",
]


def submission_to_dict(submission):
    d = {field: getattr(submission, field, None) for field in fields_nobj}
    try:
        d["author"] = {
            field: getattr(submission.author, field, False) for field in user_fields
        }
        d["author"]["subreddit"] = submission.author.subreddit.display_name
    except prawcore.exceptions.NotFound as e:
        d["author_name"] = submission.author.name
    except AttributeError as e:
        d["author_subreddit"] = None
    d["subreddit"] = submission.subreddit.display_name
    return d


def search_submissions_in_subreddit(subreddit, search_query):
    all_submissions = []
    last_submission_id = None
    while True:
        params = {"limit": 100}
        if last_submission_id is not None:
            params["after"] = f"t3_{last_submission_id}"
        result = list(
            reddit.subreddit(subreddit).search(search_query, sort="new", params=params)
        )
        if len(result) == 0:
            break
        for submission in result:
            all_submissions.append(submission_to_dict(submission))
        last_submission_id = submission.id
    return all_submissions


def search_submissions_in_mental_health(search_query):
    all_submissions = []
    for i, subreddit in enumerate(mental_subs):
        subreddit_res = search_submissions_in_subreddit(
            search_query=search_query, subreddit=subreddit
        )
        all_submissions.extend(subreddit_res)
        print(
            f"Got {len(subreddit_res)} submissions from {subreddit} subreddit, {i + 1} from {len(mental_subs)}: {(i + 1) / len(mental_subs) * 100:.2f}% progress"
        )
    return pd.json_normalize(all_submissions, sep="_")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search a query in Reddit communities related to mental health"
    )
    parser.add_argument("-query", default="chatgpt")
    args = parser.parse_args()

    df = search_submissions_in_mental_health(args.query)
    df.to_csv(f"{args.query}.csv")
