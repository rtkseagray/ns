import json
import random
from urllib.request import Request
from urllib.request import urlopen

from nationstates import Nationstates
from nationstates.objects import NSDict

NATION = 'Randomoria'
PASSWORD = ''
WEBHOOK = ''

def lambda_handler(event, context):
  _ = event, context
  api = Nationstates(f'{NATION} Decision Engine')
  nation = api.nation(NATION, password=PASSWORD)
  shard = nation.request(['issues'], None)
  issues = (shard.get('issues') or {}).get('issue', [])
  if isinstance(issues, NSDict):
    issues = [issues]

  for issue in issues:
    choice = random.choice(issue.get('option', []))
    r = nation.pick_issue(issue['id'], choice['id'])
    urlopen(
      Request(
        WEBHOOK,
        data=json.dumps({'text': f'In {NATION}, {r}'}).encode('utf-8')
      )
    )

  return {
    'statusCode': 200,
  }


