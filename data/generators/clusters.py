import uuid

CLUSTERS = [
    {
        "label": "Export Feature Confusion",
        "feature_area": "data-export",
        "example_messages": [
            "I can't find the export feature anywhere in the dashboard",
            "The export button seems to have disappeared after the update",
            "How do I download my data? I've looked everywhere",
            "Export CSV option is missing from the reports page",
            "Where did the bulk export go? I used it last week",
        ],
        "auto_summary": "Users are struggling to locate the data export feature. 73% of confused users mention 'export' or 'download' in support tickets. The feature was moved during the v2.3 redesign but navigation hints were not updated.",
        "suggested_fix": "Add an 'Export' shortcut to the top-right toolbar and include a migration tooltip for users who last used the old export location.",
    },
    {
        "label": "Team Invite Flow Broken",
        "feature_area": "team-management",
        "example_messages": [
            "Team invite link doesn't seem to work for my colleagues",
            "I'm trying to add a team member but the option is grayed out",
            "How do I share access with my team? The invite button does nothing",
            "Sent 3 invites but nobody received them",
            "Team settings page shows 'upgrade required' but I'm already on Pro",
        ],
        "auto_summary": "Team invite flow has multiple friction points. Free-tier users see the invite button but get a confusing 'upgrade' message. Pro users report invite emails landing in spam. The grayed-out state lacks explanation.",
        "suggested_fix": "Hide invite button for free tier (show upgrade CTA instead). Add email delivery status tracking. Show clear tooltip explaining grayed-out states.",
    },
    {
        "label": "API Key Management Unclear",
        "feature_area": "developer-tools",
        "example_messages": [
            "Where do I find my API key?",
            "I regenerated my key and now nothing works",
            "The API docs say to use a bearer token but I only see an API key",
            "How many API keys can I have?",
            "Is there a way to create read-only API keys?",
        ],
        "auto_summary": "Developer users are confused about API key lifecycle and permissions. The docs reference 'bearer tokens' but the UI shows 'API keys'. Key regeneration has no warning about invalidating the old key.",
        "suggested_fix": "Unify terminology to 'API keys' everywhere. Add a confirmation dialog for key regeneration with impact warning. Add scoped key support (read-only, write, admin).",
    },
]


def generate_clusters() -> list[dict]:
    return [
        {
            "cluster_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, c["label"])),
            "label": c["label"],
            "feature_area": c["feature_area"],
            "message_count": len(c["example_messages"]) * 12,
            "example_messages": c["example_messages"],
            "auto_summary": c["auto_summary"],
            "suggested_fix": c["suggested_fix"],
        }
        for c in CLUSTERS
    ]
