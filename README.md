# User Check

## Quick Start

1. Install [Slack CLI](https://api.slack.com/automation/quickstart)
2. Install python 3.11
3. Install pipenv
4. Run `pipenv run login` to get a Slack API token.
5. Copy `.env.example` to `.env` and update accordingly.
6. Run `pipenv run diff` to run the process.  Won't show a diff
   until the second time you run it.  Prints an alert if more than
   `$LOG_THRESHOLD` users have been updated (does not include
   `updated_date`).
