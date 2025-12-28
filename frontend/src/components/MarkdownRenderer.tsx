import React from "react";

interface MarkdownRendererProps {
    content: string;
    className?: string;
}

/**
 * Lightweight markdown renderer for chat messages.
 * Supports: bold, italic, inline code, headers, bullet lists, numbered lists.
 */
const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content, className = "" }) => {
    const renderMarkdown = (text: string): React.ReactNode[] => {
        const lines = text.split("\n");
        const elements: React.ReactNode[] = [];
        let listItems: React.ReactNode[] = [];
        let listType: "ul" | "ol" | null = null;
        let key = 0;

        const flushList = () => {
            if (listItems.length > 0 && listType) {
                if (listType === "ul") {
                    elements.push(<ul key={`list-${key++}`} className="md-list">{listItems}</ul>);
                } else {
                    elements.push(<ol key={`list-${key++}`} className="md-list">{listItems}</ol>);
                }
                listItems = [];
                listType = null;
            }
        };

        const parseInline = (line: string): React.ReactNode[] => {
            const result: React.ReactNode[] = [];
            let remaining = line;
            let inlineKey = 0;

            // Process inline patterns
            const patterns = [
                // Bold: **text** or __text__
                {
                    regex: /\*\*(.+?)\*\*|__(.+?)__/g, render: (match: string, g1: string, g2: string) =>
                        <strong key={`b-${inlineKey++}`}>{g1 || g2}</strong>
                },
                // Italic: *text* or _text_ (not already bold)
                {
                    regex: /(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)|(?<!_)_(?!_)(.+?)(?<!_)_(?!_)/g, render: (match: string, g1: string, g2: string) =>
                        <em key={`i-${inlineKey++}`}>{g1 || g2}</em>
                },
                // Inline code: `code`
                {
                    regex: /`([^`]+)`/g, render: (match: string, g1: string) =>
                        <code key={`c-${inlineKey++}`} className="md-code">{g1}</code>
                },
            ];

            // Simple inline parsing - handle bold, italic, code
            const parts: React.ReactNode[] = [];
            let lastIndex = 0;

            // Combined regex for all inline patterns
            const combinedRegex = /(\*\*(.+?)\*\*)|(__(.+?)__)|(`([^`]+)`)|(\*([^*]+)\*)|(_([^_]+)_)/g;
            let match;

            while ((match = combinedRegex.exec(remaining)) !== null) {
                // Add text before match
                if (match.index > lastIndex) {
                    parts.push(remaining.slice(lastIndex, match.index));
                }

                // Determine which pattern matched
                if (match[2]) {
                    // **bold**
                    parts.push(<strong key={`s-${inlineKey++}`}>{match[2]}</strong>);
                } else if (match[4]) {
                    // __bold__
                    parts.push(<strong key={`s-${inlineKey++}`}>{match[4]}</strong>);
                } else if (match[6]) {
                    // `code`
                    parts.push(<code key={`c-${inlineKey++}`} className="md-code">{match[6]}</code>);
                } else if (match[8]) {
                    // *italic*
                    parts.push(<em key={`e-${inlineKey++}`}>{match[8]}</em>);
                } else if (match[10]) {
                    // _italic_
                    parts.push(<em key={`e-${inlineKey++}`}>{match[10]}</em>);
                }

                lastIndex = match.index + match[0].length;
            }

            // Add remaining text
            if (lastIndex < remaining.length) {
                parts.push(remaining.slice(lastIndex));
            }

            return parts.length > 0 ? parts : [remaining];
        };

        for (const line of lines) {
            const trimmed = line.trim();

            // Empty line - flush list and add break
            if (!trimmed) {
                flushList();
                elements.push(<br key={`br-${key++}`} />);
                continue;
            }

            // Headers
            if (trimmed.startsWith("### ")) {
                flushList();
                elements.push(
                    <h4 key={`h4-${key++}`} className="md-header">
                        {parseInline(trimmed.slice(4))}
                    </h4>
                );
                continue;
            }
            if (trimmed.startsWith("## ")) {
                flushList();
                elements.push(
                    <h3 key={`h3-${key++}`} className="md-header">
                        {parseInline(trimmed.slice(3))}
                    </h3>
                );
                continue;
            }

            // Bullet list
            if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
                if (listType !== "ul") {
                    flushList();
                    listType = "ul";
                }
                listItems.push(
                    <li key={`li-${key++}`}>{parseInline(trimmed.slice(2))}</li>
                );
                continue;
            }

            // Numbered list
            const numberedMatch = trimmed.match(/^(\d+)\.\s+(.*)$/);
            if (numberedMatch) {
                if (listType !== "ol") {
                    flushList();
                    listType = "ol";
                }
                listItems.push(
                    <li key={`li-${key++}`}>{parseInline(numberedMatch[2])}</li>
                );
                continue;
            }

            // Regular paragraph
            flushList();
            elements.push(
                <p key={`p-${key++}`} className="md-paragraph">
                    {parseInline(trimmed)}
                </p>
            );
        }

        // Final flush
        flushList();

        return elements;
    };

    return (
        <div className={`markdown-content ${className}`}>
            {renderMarkdown(content)}
        </div>
    );
};

export default MarkdownRenderer;
