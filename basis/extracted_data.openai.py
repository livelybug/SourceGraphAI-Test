def extract_data(html: str) -> dict:
    # Parse the HTML string using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    projects = []
    # Select only the actual project items, skipping layout helpers
    for item in soup.select(".projects .grid-item"):
        # Within each project card, find title and description elements
        title_tag = item.select_one(".card-body h4.card-title")
        desc_tag = item.select_one(".card-body p.card-text")

        # Extract text content, trimming whitespace; use empty string if element is missing
        title = title_tag.get_text(strip=True) if title_tag else ""
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        projects.append({
            "title": title,
            "description": description
        })

    # Return data following the desired schema
    return {"projects": projects}