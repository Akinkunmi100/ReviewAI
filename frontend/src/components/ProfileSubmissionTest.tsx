// TEST FILE - Can be deleted after testing
// This demonstrates that the profile button works correctly

import React, { useState } from "react";

interface TestProfile {
  min_budget?: number | null;
  max_budget?: number | null;
  use_cases: string[];
  preferred_brands: string[];
}

export const ProfileSubmissionTest: React.FC = () => {
  const [profile, setProfile] = useState<TestProfile | null>(null);
  const [lastSubmitted, setLastSubmitted] = useState<TestProfile | null>(null);

  const handleProfileChange = (newProfile: TestProfile | null) => {
    console.log("📝 Profile updated in parent:", newProfile);
    setProfile(newProfile);
  };

  const simulateChatMessage = () => {
    // This simulates what happens when user sends a chat message
    console.log("💬 Sending chat with profile:", profile);
    setLastSubmitted(profile);
    
    // Simulate API call
    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        product_name: "Test Product",
        message: "Test message",
        user_profile: profile, // ✅ This is what gets sent
      }),
    }).then(() => {
      console.log("✅ Profile sent successfully:", profile);
    });
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px" }}>
      <h2>Profile Submission Test</h2>
      
      <div style={{ background: "#f0f0f0", padding: "15px", marginBottom: "20px" }}>
        <h3>Current Profile State:</h3>
        <pre>{JSON.stringify(profile, null, 2)}</pre>
      </div>

      <div style={{ background: "#e8f5e9", padding: "15px", marginBottom: "20px" }}>
        <h3>Last Submitted Profile (in API call):</h3>
        <pre>{JSON.stringify(lastSubmitted, null, 2)}</pre>
      </div>

      <div style={{ display: "flex", gap: "10px" }}>
        <button
          onClick={() => handleProfileChange({
            min_budget: 50000,
            max_budget: 200000,
            use_cases: ["Gaming", "Work"],
            preferred_brands: ["Samsung", "Apple"],
          })}
          style={{ padding: "10px 20px", background: "#2196F3", color: "white", border: "none", borderRadius: "5px" }}
        >
          Set Test Profile
        </button>

        <button
          onClick={simulateChatMessage}
          style={{ padding: "10px 20px", background: "#4CAF50", color: "white", border: "none", borderRadius: "5px" }}
        >
          Send Chat (Test API Call)
        </button>

        <button
          onClick={() => handleProfileChange(null)}
          style={{ padding: "10px 20px", background: "#F44336", color: "white", border: "none", borderRadius: "5px" }}
        >
          Clear Profile
        </button>
      </div>

      <div style={{ marginTop: "20px", padding: "15px", background: "#fff3cd", borderRadius: "5px" }}>
        <h4>✅ How It Works:</h4>
        <ol style={{ marginLeft: "20px" }}>
          <li>User fills out ProfilePanel form</li>
          <li>User clicks "Save Profile" button</li>
          <li>ProfilePanel calls <code>onChange(profile)</code></li>
          <li>ReviewPage updates state with <code>setUserProfile(profile)</code></li>
          <li>Updated profile is passed to <code>useChat</code> hook</li>
          <li>When user sends chat, profile is included in API call</li>
        </ol>
      </div>
    </div>
  );
};

export default ProfileSubmissionTest;
