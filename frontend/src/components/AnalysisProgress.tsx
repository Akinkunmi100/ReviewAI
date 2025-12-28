import React, { useEffect, useState } from "react";
import { Search, Globe, Brain, DollarSign, Sparkles, CheckCircle } from "lucide-react";

interface Props {
    isLoading: boolean;
    productName: string;
}

const ANALYSIS_STEPS = [
    { id: 1, label: "Searching the web...", icon: Search, duration: 3000 },
    { id: 2, label: "Fetching product data...", icon: Globe, duration: 5000 },
    { id: 3, label: "Generating AI review...", icon: Brain, duration: 8000 },
    { id: 4, label: "Comparing prices...", icon: DollarSign, duration: 4000 },
    { id: 5, label: "Analyzing sentiment & features...", icon: Sparkles, duration: 3000 },
];

const AnalysisProgress: React.FC<Props> = ({ isLoading, productName }) => {
    const [currentStep, setCurrentStep] = useState(0);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        if (!isLoading) {
            setCurrentStep(0);
            setProgress(0);
            return;
        }

        // Start the step animation
        let stepIndex = 0;
        const stepIntervals: ReturnType<typeof setTimeout>[] = [];

        const advanceStep = () => {
            if (stepIndex < ANALYSIS_STEPS.length) {
                setCurrentStep(stepIndex + 1);
                stepIndex++;

                if (stepIndex < ANALYSIS_STEPS.length) {
                    stepIntervals.push(setTimeout(advanceStep, ANALYSIS_STEPS[stepIndex - 1].duration));
                }
            }
        };

        advanceStep();

        // Progress bar animation
        const progressInterval = setInterval(() => {
            setProgress((prev) => {
                if (prev >= 95) return prev; // Cap at 95% until complete
                return prev + 1;
            });
        }, 250);

        return () => {
            stepIntervals.forEach(clearTimeout);
            clearInterval(progressInterval);
        };
    }, [isLoading]);

    if (!isLoading) return null;

    return (
        <div className="analysis-progress-container">
            <div className="analysis-progress-card">
                <div className="analysis-progress-header">
                    <h3>Analyzing "{productName}"</h3>
                    <span className="analysis-progress-percent">{Math.min(progress, 95)}%</span>
                </div>

                <div className="analysis-progress-bar-container">
                    <div
                        className="analysis-progress-bar"
                        style={{ width: `${Math.min(progress, 95)}%` }}
                    />
                </div>

                <div className="analysis-steps-list">
                    {ANALYSIS_STEPS.map((step, index) => {
                        const StepIcon = step.icon;
                        const isActive = currentStep === index + 1;
                        const isComplete = currentStep > index + 1;

                        return (
                            <div
                                key={step.id}
                                className={`analysis-step ${isActive ? 'active' : ''} ${isComplete ? 'complete' : ''}`}
                            >
                                <div className="analysis-step-icon">
                                    {isComplete ? (
                                        <CheckCircle size={18} />
                                    ) : (
                                        <StepIcon size={18} />
                                    )}
                                </div>
                                <span className="analysis-step-label">{step.label}</span>
                                {isActive && <span className="analysis-step-dots">...</span>}
                            </div>
                        );
                    })}
                </div>

                <p className="analysis-progress-note">
                    This usually takes 15-30 seconds depending on data availability.
                </p>
            </div>
        </div>
    );
};

export default AnalysisProgress;
