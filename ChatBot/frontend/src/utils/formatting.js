



export function parseFormattedText(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")     // bold
    .replace(/\n/g, "<br/>")                               // line breaks
    .replace(/^\d+\.\s(.*)$/gm, "<li>$1</li>")             // numbered list
    .replace(/^- (.*)$/gm, "<li>$1</li>")                  // bullet list
    .replace(/(<li>.*<\/li>)/g, "<ul>$1</ul>");            // wrap in <ul>
}