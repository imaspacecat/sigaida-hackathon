import React from 'react';

interface Campaign {
    id: number;
    name: string;
    description: string;
}

interface CampaignListProps {
    campaigns: Campaign[];
    onCampaignClick: (campaign: Campaign) => void;
}

const CampaignList: React.FC<CampaignListProps> = ({ campaigns, onCampaignClick }) => (
    <div style={styles.campaignList}>
        <h2 style={styles.campaignTitle}>Matching Campaigns</h2>
        <ul style={styles.campaignItemList}>
            {campaigns.map(campaign => (
                <li
                    key={campaign.id}
                    style={styles.campaignItem}
                    onClick={() => onCampaignClick(campaign)}
                >
                    {campaign.name}
                </li>
            ))}
        </ul>
    </div>
);

const styles: { [key: string]: React.CSSProperties } = {
    campaignList: {
        width: '90%',
        height: '90%',
        backgroundColor: '#ffffff',
        borderRadius: '20px',
        padding: '20px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        overflowY: 'auto',
    },
    campaignTitle: {
        fontSize: '1.5rem',
        fontWeight: 'bold',
        color: '#4A3A57',
        marginBottom: '15px',
    },
    campaignItemList: {
        listStyleType: 'none',
        padding: 0,
        margin: 0,
    },
    campaignItem: {
        padding: '12px 20px',
        margin: '10px 0',
        borderRadius: '15px',
        backgroundColor: '#D8B4E2',
        color: '#4A3A57',
        fontSize: '1.2rem',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'background-color 0.3s',
    },
};

export default CampaignList;