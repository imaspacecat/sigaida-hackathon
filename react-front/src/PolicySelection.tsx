import React from 'react';

interface Policy {
    id: number;
    name: string;
    userChoice: number; // Ensure this is a number for use with the range input
}

interface PolicySelectionProps {
    policies: Policy[];
    updatePolicyChoice: (id: number, choice: number) => void;
}

const PolicySelection: React.FC<PolicySelectionProps> = ({ policies, updatePolicyChoice }) => {
    return (
        <div style={styles.policySelection}>
            <h2 style={styles.title}>You support these policies:</h2>
            <ul style={styles.policyList}>
                {policies.map(policy => (
                    <li key={policy.id} style={styles.policyItem}>
                        <span style={styles.policyName}>{policy.name}</span>
                        <div style={styles.sliderContainer}>
                            <input
                                type="range"
                                min="-100"
                                max="100"
                                value={policy.userChoice}
                                onChange={(e) => updatePolicyChoice(policy.id, Number(e.target.value))}
                                style={styles.slider}
                            />
                            <span style={styles.policyValue}>
                                {policy.userChoice > 0
                                    ? "Support"
                                    : policy.userChoice < 0
                                    ? "Oppose"
                                    : "Neutral"}
                            </span>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

const styles: { [key: string]: React.CSSProperties } = {
    policySelection: {
        width: '100%',
        backgroundColor: '#D8B4E2',
        borderRadius: '20px',
        padding: '20px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        overflowY: 'auto',
    },
    title: {
        fontSize: '1.5rem',
        fontWeight: 'bold',
        color: '#ffffff',
        textAlign: 'center',
        marginBottom: '10px',
    },
    policyList: {
        listStyleType: 'none',
        padding: 0,
        margin: 0,
    },
    policyItem: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '10px 0',
        borderBottom: '1px solid #cccccc',
    },
    policyName: {
        flex: 1,
        color: '#4A3A57',
        fontWeight: 'bold',
    },
    sliderContainer: {
        display: 'flex',
        alignItems: 'center',
        width: '60%',
    },
    slider: {
        flex: 1,
        marginRight: '10px',
    },
    policyValue: {
        width: '70px',
        textAlign: 'center',
        fontWeight: 'bold',
        color: '#4A3A57',
    },
};

export default PolicySelection;