import React, { useState, useEffect } from "react";
import { apiSaveProfile } from "../api/client";

export interface UserProfile {
  min_budget?: number | null;
  max_budget?: number | null;
  use_cases: string[];
  preferred_brands: string[];
}

interface Props {
  value: UserProfile | null;
  onChange: (p: UserProfile | null) => void;
  userId?: string;
  isLoading?: boolean;
}

const ALL_USE_CASES = [
  "Gaming",
  "Work",
  "Photography",
  "Travel",
  "Students",
  "Content Creation",
  "Fitness",
  "Music",
];

const ProfilePanel: React.FC<Props> = ({ value, onChange, userId, isLoading }) => {
  // Local state for form inputs
  const [minBudget, setMinBudget] = useState<number | "">(value?.min_budget ?? "");
  const [maxBudget, setMaxBudget] = useState<number | "">(value?.max_budget ?? "");
  const [useCases, setUseCases] = useState<string[]>(value?.use_cases ?? []);
  const [preferred, setPreferred] = useState<string>(
    (value?.preferred_brands ?? []).join(", "),
  );
  const [customUseCases, setCustomUseCases] = useState<string>("");

  // State for tracking changes and showing feedback
  const [hasChanges, setHasChanges] = useState<boolean>(false);
  const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "saved">("idle");
  const [validationError, setValidationError] = useState<string>("");

  // Track if form values have changed from the saved profile
  useEffect(() => {
    const currentProfile = {
      min_budget: minBudget === "" ? null : Number(minBudget),
      max_budget: maxBudget === "" ? null : Number(maxBudget),
      use_cases: useCases,
      preferred_brands: preferred
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    };

    const hasChanged = JSON.stringify(currentProfile) !== JSON.stringify(value || {
      min_budget: null,
      max_budget: null,
      use_cases: [],
      preferred_brands: [],
    });

    setHasChanges(hasChanged);

    // Clear save status when user makes changes after saving
    if (hasChanged && saveStatus === "saved") {
      setSaveStatus("idle");
    }
  }, [minBudget, maxBudget, useCases, preferred, value, saveStatus]);

  function toggleUseCase(uc: string) {
    setUseCases((prev) =>
      prev.includes(uc) ? prev.filter((x) => x !== uc) : [...prev, uc],
    );
  }

  function validateProfile(): string {
    // Validate budget range
    if (minBudget !== "" && maxBudget !== "" && Number(minBudget) > Number(maxBudget)) {
      return "Minimum budget cannot be greater than maximum budget";
    }

    // Validate budget values are positive
    if (minBudget !== "" && Number(minBudget) < 0) {
      return "Budget values must be positive";
    }
    if (maxBudget !== "" && Number(maxBudget) < 0) {
      return "Budget values must be positive";
    }

    return "";
  }

  async function handleSaveProfile() {
    // Validate
    const error = validateProfile();
    if (error) {
      setValidationError(error);
      return;
    }

    setValidationError("");
    setSaveStatus("saving");

    // Build profile object
    const profile: UserProfile = {
      min_budget: minBudget === "" ? null : Number(minBudget),
      max_budget: maxBudget === "" ? null : Number(maxBudget),
      use_cases: useCases,
      preferred_brands: preferred
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    };

    // Call onChange to update parent
    onChange(profile);

    // If user is authenticated, call the API to persist profile
    try {
      await apiSaveProfile(profile);
    } catch (e) {
      // Swallow errors for now; feedback can be added later
      console.warn("Failed to persist profile to server", e);
    }

    // Show success feedback
    setTimeout(() => {
      setSaveStatus("saved");
      setHasChanges(false);

      // Reset to idle after 2 seconds
      setTimeout(() => {
        setSaveStatus("idle");
      }, 2000);
    }, 300);
  }

  function handleClearProfile() {
    if (window.confirm("Are you sure you want to clear your profile?")) {
      setMinBudget("");
      setMaxBudget("");
      setUseCases([]);
      setPreferred("");
      setCustomUseCases("");
      onChange(null);
      setSaveStatus("idle");
      setValidationError("");
    }
  }

  return (
    <div className="profile-panel">
      <h3>Your Profile</h3>

      <div className="profile-form">
        <label>
          Min budget (₦)
          <input
            type="number"
            value={minBudget === "" ? "" : minBudget}
            onChange={(e) =>
              setMinBudget(e.target.value === "" ? "" : Number(e.target.value))
            }
            placeholder="e.g., 50000"
          />
        </label>

        <label>
          Max budget (₦)
          <input
            type="number"
            value={maxBudget === "" ? "" : maxBudget}
            onChange={(e) =>
              setMaxBudget(e.target.value === "" ? "" : Number(e.target.value))
            }
            placeholder="e.g., 200000"
          />
        </label>

        <div className="usecases">
          <div className="usecases-header">Use cases:</div>
          <div className="usecases-grid">
            {ALL_USE_CASES.map((uc) => (
              <label
                key={uc}
                className={`usecase-chip ${useCases.includes(uc) ? "active" : ""}`}
              >
                <input
                  type="checkbox"
                  checked={useCases.includes(uc)}
                  onChange={() => toggleUseCase(uc)}
                  className="usecase-checkbox"
                />
                <span className="usecase-label">{uc}</span>
              </label>
            ))}
          </div>
          <div className="custom-input-group">
            <input
              type="text"
              value={customUseCases}
              onChange={(e) => {
                setCustomUseCases(e.target.value);
                const extra = e.target.value
                  .split(",")
                  .map((s) => s.trim())
                  .filter(Boolean);
                setUseCases((prev) => {
                  const base = prev.filter((p) => ALL_USE_CASES.includes(p));
                  return Array.from(new Set([...base, ...extra]));
                });
              }}
              placeholder="+ Add custom use case"
              className="custom-input"
            />
          </div>
        </div>

        <div className="brands-section">
          <div className="brands-header">Preferred brands:</div>
          <input
            type="text"
            value={preferred}
            onChange={(e) => setPreferred(e.target.value)}
            placeholder="e.g., Samsung, Apple, Sony"
            className="brands-input"
          />
        </div>

        {validationError && (
          <div className="validation-error">
            ⚠️ {validationError}
          </div>
        )}

        <div className="profile-actions">
          <button
            onClick={handleSaveProfile}
            disabled={!hasChanges || saveStatus === "saving"}
            className={`save-button ${!hasChanges ? "disabled" : ""} ${saveStatus === "saved" ? "success" : ""}`}
          >
            {saveStatus === "saving" && "Saving..."}
            {saveStatus === "saved" && "✓ Saved!"}
            {saveStatus === "idle" && (hasChanges ? "Save Profile" : "No Changes")}
          </button>

          <button
            onClick={handleClearProfile}
            className="clear-button"
            type="button"
          >
            Clear All
          </button>
        </div>

        {saveStatus === "saved" && (
          <div className="save-feedback">
            Profile saved! Your preferences will be used in product recommendations.
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfilePanel;
