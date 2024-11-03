import React, { useState, ChangeEvent, KeyboardEvent } from 'react';

const App: React.FC = () => {
    const [inputText, setInputText] = useState<string>('');

    const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
        const text = e.target.value;
        if (text.split(' ').length <= 150) {
            setInputText(text); 
        }
    };

    const handleSubmit = () => {
        if (inputText.trim()) {
            console.log('Submitted:', inputText);
        }
    };

    const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault(); 
            handleSubmit();
        }
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.header}>CampaignCo</h1>
            <p style={styles.subheader}>Find campaigns that align with your values</p>
            <div style={styles.inputWrapper}>
                <textarea
                    style={styles.textBox}
                    placeholder="Tell us about the policy issues you support..."
                    value={inputText}
                    onChange={handleChange}
                    onKeyDown={handleKeyPress}
                    rows={1}
                />
            </div>
            <button onClick={handleSubmit} style={styles.button}>Enter</button>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100vw',
        height: '100vh',
        background: 'linear-gradient(135deg, #6A0DAD, #D8B4E2)',
        color: '#fff',
        textAlign: 'center',
        boxSizing: 'border-box',
        margin: 0,
        padding: 0,
    } as React.CSSProperties,
    header: {
        fontSize: '2.8rem',
        fontWeight: 'bold',
        color: '#ffffff',
        marginBottom: '10px',
    } as React.CSSProperties,
    subheader: {
        fontSize: '1.2rem',
        color: '#E0CCE1',
        fontStyle: 'italic',
        marginBottom: '30px',
    } as React.CSSProperties,
    inputWrapper: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#D8B4E2', // Light purple for contrast
        borderRadius: '30px',
        border: '1px solid #ffffff',
        padding: '10px',
        width: '100%',
        maxWidth: '500px',
        boxSizing: 'border-box',
    } as React.CSSProperties,
    textBox: {
        width: '100%',
        padding: '15px',
        fontSize: '16px',
        color: '#4A3A57',
        backgroundColor: '#D8B4E2',
        border: 'none',
        borderRadius: '30px',
        outline: 'none',
        resize: 'none',
        boxSizing: 'border-box',
        fontFamily: 'inherit',
    } as React.CSSProperties,
    button: {
        marginTop: '20px',
        padding: '12px 40px',
        fontSize: '16px',
        backgroundColor: '#D8B4E2',
        color: '#4A3A57',
        border: 'none',
        borderRadius: '30px',
        cursor: 'pointer',
        fontFamily: 'inherit',
        fontWeight: 'bold',
    } as React.CSSProperties,
};

export default App;