import React from "react";
import { PlayCircle, Youtube, ExternalLink, Search } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";
import { safeArray, safeString } from "../utils/safeHelpers";

interface Props {
    review: EnhancedProductReview;
}

const VideoProof: React.FC<Props> = ({ review }) => {
    const proof = review?.video_proof;
    const moments = safeArray(proof?.moments);
    if (!proof || moments.length === 0) return null;

    return (
        <section className="video-section section-card">
            <div className="section-header">
                <div className="section-icon video-icon">
                    <Youtube size={24} />
                </div>
                <div>
                    <h3>Video Proof Finder</h3>
                    <p className="section-subtitle">Instantly verify claims with targeted video search</p>
                </div>
            </div>

            <div className="moments-list">
                {moments.map((moment, idx) => (
                    <div key={idx} className="moment-card">
                        <div className="moment-content">
                            <div className="moment-header">
                                <PlayCircle size={18} className="text-danger" />
                                <strong>{safeString(moment.label)}</strong>
                            </div>
                                <p className="moment-desc">{safeString(moment.description)}</p>
                        </div>

                        <a
                            href={safeString(moment.youtube_url, '#')}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="find-proof-btn"
                        >
                            <Search size={16} />
                            <span>Find Proof</span>
                            <ExternalLink size={12} className="ml-1 opacity-50" />
                        </a>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default VideoProof;
