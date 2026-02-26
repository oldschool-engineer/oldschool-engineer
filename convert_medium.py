"""Convert Medium HTML export files to Jekyll markdown posts."""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as md

EXPORT_DIR = Path(r"c:\Users\tom\Documents\GitHub\oldschool-engineer\medium-export\posts")
OUTPUT_DIR = Path(r"c:\Users\tom\Documents\GitHub\oldschool-engineer\_posts")

# Category and tag assignments based on content analysis
POST_METADATA = {
    "e9478f7be3a6": {
        "categories": ["Meta"],
        "tags": ["personal", "navy", "career"],
        "excerpt": "From the Apple IIe to the USS Nimitz to a 20+ year career in tech — how it all started.",
    },
    "07ab06c0e1ea": {
        "categories": ["Infrastructure"],
        "tags": ["tls", "certbot", "aws", "route53", "automation"],
        "excerpt": "Free TLS certificates with automated renewal using Certbot, Route 53, and GoCD.",
    },
    "dc35e0627674": {
        "categories": ["Side Projects"],
        "tags": ["github-pages", "javascript", "dad-jokes"],
        "excerpt": "Building a random dad joke site in an hour with vanilla HTML and zero frameworks.",
    },
    "86aa52fd27aa": {
        "categories": ["Meta"],
        "tags": ["home-lab", "budget"],
        "excerpt": "Introducing the concept of building impressive tech solutions on a budget.",
    },
    "9b009811a92c": {
        "categories": ["Home Lab"],
        "tags": ["proxmox", "networking", "home-lab", "infrastructure"],
        "excerpt": "From Raspberry Pi experiments to a full Proxmox cluster — the honest evolution of a home lab.",
    },
    "356a6ac1ca70": {
        "categories": ["AI"],
        "tags": ["mattermost", "chatbot", "prompt-engineering"],
        "excerpt": "Building Fake Spock — a Mattermost chatbot tuned to behave like a Vulcan and deliver dad jokes.",
    },
    "fe39d736ade6": {
        "categories": ["Infrastructure"],
        "tags": ["kubernetes", "aws", "bedrock", "hybrid-cloud", "cost-optimization"],
        "excerpt": "Migrating AI workloads from AWS Lambda to on-premises Kubernetes to cut costs.",
    },
    "47f2a18446f1": {
        "categories": ["Software Engineering"],
        "tags": ["vibe-coding", "llm", "ai", "brainfuck"],
        "excerpt": "A thought experiment on why Brainfuck reveals the fundamental limits of AI-assisted coding.",
    },
    "d5107b240096": {
        "categories": ["Infrastructure"],
        "tags": ["kubernetes", "litellm", "langflow", "aws", "bedrock", "hybrid-cloud"],
        "excerpt": "Self-hosting LiteLLM, Langflow, and Khoj on Kubernetes while using AWS Bedrock for inference.",
    },
    "28fc3b6d9be0": {
        "categories": ["Side Projects"],
        "tags": ["fastapi", "rabbitmq", "redis", "vue", "market-data"],
        "excerpt": "Building a real-time stock scanner with FastAPI, RabbitMQ, and Redis — Part 1.",
    },
    "94e445914951": {
        "categories": ["Side Projects"],
        "tags": ["docker", "deployment", "market-data"],
        "excerpt": "Running the stock scanner with Docker Compose — setup, configuration, and first launch.",
    },
    "eab7d9bbf5f7": {
        "categories": ["Infrastructure"],
        "tags": ["kubernetes", "ansible", "deployment", "market-data"],
        "excerpt": "From Docker Compose to production Kubernetes with Ansible, MetalLB, and cert-manager.",
    },
    "408779a1f3f2": {
        "categories": ["Software Engineering"],
        "tags": ["opentelemetry", "observability", "performance", "market-data"],
        "excerpt": "How OpenTelemetry exposed a hidden bottleneck and drove architectural improvements.",
    },
    "a9209c4230ac": {
        "categories": ["Software Engineering"],
        "tags": ["python", "asyncio", "redis", "caching", "performance"],
        "excerpt": "A two-layer cache-miss prevention strategy using asyncio.Event and Redis locks.",
    },
    "5b1360b64921": {
        "categories": ["Software Engineering"],
        "tags": ["testing", "documentation", "performance", "market-data"],
        "excerpt": "Wrapping up Wave 1 — debugging stories, 1,490 msg/s throughput, and 100% test coverage.",
    },
}


def extract_medium_id(filename):
    """Extract the Medium post ID from the filename (last segment before .html)."""
    match = re.search(r'-([a-f0-9]+)\.html$', filename)
    return match.group(1) if match else None


def extract_date(filename):
    """Extract the date from the filename."""
    match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    return match.group(1) if match else None


def slugify(title):
    """Convert a title to a URL-friendly slug."""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def convert_html_to_markdown(html_content):
    """Convert Medium export HTML to clean markdown."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title_tag = soup.find('h1', class_='p-name')
    title = title_tag.get_text().strip() if title_tag else "Untitled"

    # Extract body content
    body = soup.find('section', {'data-field': 'body'})
    if not body:
        return title, ""

    # Remove the duplicate title (h3 with graf--title class)
    title_h3 = body.find('h3', class_='graf--title')
    if title_h3:
        title_h3.decompose()

    # Remove section dividers that are just decoration
    for divider_div in body.find_all('div', class_='section-divider'):
        divider_div.decompose()

    # Convert images to markdown-friendly format
    for figure in body.find_all('figure'):
        img = figure.find('img')
        caption = figure.find('figcaption')
        if img:
            src = img.get('src', '')
            alt = img.get('alt', '')
            caption_text = caption.get_text().strip() if caption else ''
            if caption_text:
                figure.replace_with(BeautifulSoup(
                    f'<p><img src="{src}" alt="{alt}"></p><p><em>{caption_text}</em></p>',
                    'html.parser'
                ))
            else:
                figure.replace_with(BeautifulSoup(
                    f'<p><img src="{src}" alt="{alt}"></p>',
                    'html.parser'
                ))

    # Convert to markdown
    markdown = md(str(body), heading_style="ATX", code_language="python")

    # Clean up excessive whitespace
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = markdown.strip()

    return title, markdown


def convert_post(filepath):
    """Convert a single Medium HTML file to a Jekyll markdown post."""
    filename = filepath.name
    medium_id = extract_medium_id(filename)
    date = extract_date(filename)

    if not medium_id or not date:
        print(f"  Skipping {filename}: could not extract ID or date")
        return

    metadata = POST_METADATA.get(medium_id,  {
        "categories": ["Uncategorized"],
        "tags": [],
        "excerpt": "",
    })

    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    title, markdown_body = convert_html_to_markdown(html_content)

    # Build front matter
    front_matter = f'---\ntitle: "{title}"\n'
    if metadata.get("excerpt"):
        front_matter += f'excerpt: "{metadata["excerpt"]}"\n'
    front_matter += f'categories:\n'
    for cat in metadata["categories"]:
        front_matter += f'  - {cat}\n'
    front_matter += f'tags:\n'
    for tag in metadata["tags"]:
        front_matter += f'  - {tag}\n'
    front_matter += '---\n'

    # Build output filename
    slug = slugify(title)
    output_filename = f"{date}-{slug}.md"
    output_path = OUTPUT_DIR / output_filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write('\n')
        f.write(markdown_body)
        f.write('\n')

    print(f"  {filename} -> {output_filename}")


def main():
    print(f"Converting Medium posts from: {EXPORT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    html_files = sorted(EXPORT_DIR.glob("*.html"))
    print(f"Found {len(html_files)} posts to convert.\n")

    for filepath in html_files:
        convert_post(filepath)

    print(f"\nDone. Converted {len(html_files)} posts.")


if __name__ == "__main__":
    main()
