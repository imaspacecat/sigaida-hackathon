import React, { useState } from 'react';
import StartingPage from './StartingPage';
import PolicySelection from './PolicySelection';
import CampaignList from './CampaignList';
import CampaignDetail from './CampaignDetail';

interface Policy {
    id: number;
    name: string;
    userChoice: number; // Make sure this is a number to align with slider values
}

interface Campaign {
    id: number;
    name: string;
    description: string;
}

const initialPolicies: Policy[] = [
    { id: 1, name: "Pro-Choice", userChoice: 0 },
    { id: 2, name: "Requiring ID to Vote", userChoice: 0 },
    { id: 3, name: "Gun-Control", userChoice: 0 },
];

const placeholderCampaigns: Campaign[] = [
    { id: 1, name: "Campaign A", description: "Details about Campaign A" },
    { id: 2, name: "Campaign B", description: "Details about Campaign B" },
];

const App: React.FC = () => {
    const [isMainScreen, setIsMainScreen] = useState(false);
    const [inputText, setInputText] = useState<string>('');
    const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null);
    const [policies, setPolicies] = useState<Policy[]>(initialPolicies);

    const handleStart = async () => {
        // Send the user input to the backend to analyze sentiment
        try {
            const response = await fetch("http://127.0.0.1:5000/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: inputText })
            });
            
            if (!response.ok) {
                throw new Error("Failed to analyze sentiment");
            }
            
            const sentiments = await response.json();
            
            // Map response to update the policy sliders
            setPolicies(prevPolicies =>
                prevPolicies.map(policy => {
                    const sentiment = sentiments.find((s: any) => s.policy.toLowerCase() === policy.name.toLowerCase());
                    return {
                        ...policy,
                        userChoice: sentiment ? sentiment.score : 0 // Update score from sentiment analysis
                    };
                })
            );
            
            setIsMainScreen(true); // Move to the main screen
        } catch (error) {
            console.error("Error analyzing sentiment:", error);
        }
    };

    const handleCampaignClick = (campaign: Campaign) => setSelectedCampaign(campaign);
    const handleBackClick = () => setSelectedCampaign(null);

    const updatePolicyChoice = (id: number, choice: number) => {
        setPolicies(prevPolicies =>
            prevPolicies.map(policy =>
                policy.id === id ? { ...policy, userChoice: choice } : policy
            )
        );
    };

    return (
        <div style={styles.appContainer}>
            {!isMainScreen ? (
                <StartingPage
                    inputText={inputText}
                    setInputText={setInputText}
                    onSubmit={handleStart}
                />
            ) : selectedCampaign ? (
                <CampaignDetail campaign={selectedCampaign} onBackClick={handleBackClick} />
            ) : (
                <div style={styles.mainContent}>
                    <div style={styles.leftPanel}>
                        <PolicySelection policies={policies} updatePolicyChoice={updatePolicyChoice} />
                    </div>
                    <div style={styles.rightPanel}>
                        <CampaignList campaigns={placeholderCampaigns} onCampaignClick={handleCampaignClick} />
                    </div>
                </div>
            )}
        </div>
    );
};

const styles: { [key: string]: React.CSSProperties } = {
    appContainer: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        width: '100vw',
        height: '100vh',
        backgroundColor: '#2e2e2e',
    },
    mainContent: {
        display: 'flex',
        width: '90%',
        height: '90%',
    },
    leftPanel: {
        flex: '1',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '10px',
        boxSizing: 'border-box',
    },
    rightPanel: {
        flex: '2',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '10px',
        boxSizing: 'border-box',
    },
};

export default App;