import React from 'react';

interface Campaign {
    id: number;
    name: string;
    description: string;
}

interface CampaignDetailProps {
    campaign: Campaign;
    onBackClick: () => void;
}

const CampaignDetail: React.FC<CampaignDetailProps> = ({ campaign, onBackClick }) => (
    <div style={styles.campaignDetail}>
        <button onClick={onBackClick} style={styles.backButton}>← Back</button>
        <h2 style={styles.campaignTitle}>{campaign.name}</h2>
        <p style={styles.campaignDescription}>{campaign.description}</p>
    </div>
);

const styles: { [key: string]: React.CSSProperties } = {
    campaignDetail: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        backgroundColor: '#6A0DAD',
        color: '#ffffff',
        textAlign: 'center',
        padding: '20px',
    },
    backButton: {
        position: 'absolute',
        top: '20px',
        left: '20px',
        padding: '10px 20px',
        fontSize: '1rem',
        backgroundColor: '#D8B4E2',
        color: '#4A3A57',
        border: 'none',
        borderRadius: '15px',
        cursor: 'pointer',
    },
    campaignTitle: {
        fontSize: '2rem',
        fontWeight: 'bold',
        color: '#ffffff',
        marginBottom: '20px',
    },
    campaignDescription: {
        fontSize: '1.2rem',
        lineHeight: '1.6',
        maxWidth: '600px',
        color: '#E0CCE1',
    },
};

export default CampaignDetail;