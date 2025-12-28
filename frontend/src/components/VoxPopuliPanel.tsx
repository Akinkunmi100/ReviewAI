import React from "react";
import { MessageSquare, ThumbsUp, ThumbsDown, MessageCircle } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";
import { safeArray, safeString } from "../utils/safeHelpers";

interface Props {
    review: EnhancedProductReview;
}

const VoxPopuliPanel: React.FC<Props> = ({ review }) => {
    const report = review?.vox_populi_report;
    if (!report) return null;
    const love = safeArray(report.love_it_for);
    const hate = safeArray(report.hate_it_for);
    const forum = safeArray(report.forum_consensus);

    return (
        <section className="vox-populi-section section-card">
            <div className="section-header">
                <div className="section-icon vox-icon">
                    <MessageSquare size={24} />
                </div>
                <div>
                    <h3>The Vox Populi</h3>
                    <p className="section-subtitle">Real owner consensus from Nairaland, Reddit & Twitter</p>
                </div>
            </div>

            <div className="vox-grid">
                {/* Main Verdict */}
                <div className="vox-card verdict-card">
                    <h4>"The Street Verdict"</h4>
                    <p className="verdict-quote">"{safeString(report.owner_verdict, 'No verdict')}"</p>
                </div>

                {/* Love / Hate Lists */}
                <div className="vox-split">
                    <div className="vox-list-card love-card">
                        <h4 className="vox-list-header text-success">
                            <ThumbsUp size={16} />
                            Owners Love
                        </h4>
                        <ul>
                            {love.map((item, i) => (
                                <li key={i}>{item}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="vox-list-card hate-card">
                        <h4 className="vox-list-header text-danger">
                            <ThumbsDown size={16} />
                            Owners Hate
                        </h4>
                        <ul>
                            {hate.map((item, i) => (
                                <li key={i}>{item}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            {/* Forum Breakdown */}
            <h4 className="subsection-title mt-4">
                <MessageCircle size={18} />
                Forum Breakdown
            </h4>
            <div className="forum-grid">
                {forum.map((opinion, idx) => (
                    <div key={idx} className="forum-card">
                        <div className="forum-header">
                            <span className={`platform-badge ${(opinion.platform ?? '').toLowerCase()}`}>
                                {opinion.platform ?? ''}
                            </span>
                            <span className={`sentiment-badge ${(opinion.sentiment ?? '').toLowerCase()}`}>
                                {opinion.sentiment ?? ''}
                            </span>
                        </div>
                        <p className="forum-takeaway">"{opinion.key_takeaway}"</p>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default VoxPopuliPanel;
