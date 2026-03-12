"""
Move documentation files to docs folder
"""

# README
with open('../README.md') as f:
    readme_content = f.read()

# BLOG_ARTICLE
with open('../BLOG_ARTICLE.md') as f:
    blog_content = f.read()

print("Documentation files are ready to be moved to the docs folder.")
