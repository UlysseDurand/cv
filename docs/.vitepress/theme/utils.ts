// Convert markdown [text](url) to <a href="url">text</a>
export function mdLinksToHtml(text: string): string {
  if (!text) return text
  return text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
}

// Transform links from object {label: url} to array [{label, url}]
export function transformLinks(linksObj: Record<string, string> | undefined): Array<{ label: string; url: string }> {
  if (!linksObj) return []
  return Object.entries(linksObj).map(([label, url]) => ({ label, url }))
}
