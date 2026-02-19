from datetime import datetime, timezone
from core.mongo import MongoDBClient
from .constants import IssueStatus

db = MongoDBClient.get_db()
issues_col = db["issues"]

def update_overdue_issues():
    now = datetime.now(timezone.utc)

    issues = issues_col.find({
        "status": IssueStatus.ISSUED,
        "due_date": {"$lt": now}
    })

    for issue in issues:
        issues_col.update_one(
            {"uuid": issue["uuid"]},
            {"$set": {"status": IssueStatus.OVERDUE}}
        )
