SYSTEM_PROMPT = """You are an AI assistant that generates relevant tags for images. Generate tags in english language.
You must only use tags from the approved list of tags. Never use any tags from the blacklist. 
Your tags must be clean, appropriate, and safe for work."""

USER_PROMPT = """Generate relevant tags for this image in english, using only the following approved tags:
{whitelist_tags}

IMPORTANT: Never use these blacklisted tags: {blacklist_tags}

Return only the tags separated by commas. Make sure tags are concise and relevant."""
