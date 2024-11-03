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
            <h1 style={styles.header}>PoliDonor</h1>
            <div style={styles.inputWrapper}>
                <textarea
                    style={styles.textBox}
                    placeholder="Tell us about the policy issues you support..."
                    value={inputText}
                    onChange={handleChange}
                    onKeyDown={handleKeyPress}
                    rows={4}
                />
                <button onClick={handleSubmit} style={styles.button}>Enter</button>
            </div>
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
        backgroundColor: '#E84A27',
        color: '#fff',
        textAlign: 'center',
        margin: 0,
        padding: 0,
        boxSizing: 'border-box',
    } as React.CSSProperties,
    header: {
        fontSize: '2.5rem',
        marginBottom: '20px',
        color: '#ffffff',
    } as React.CSSProperties,
    inputWrapper: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#333',
        borderRadius: '20px',
        border: '1px solid #ffffff',
        padding: '10px',
        width: '100%',
        maxWidth: '500px',
        boxSizing: 'border-box',
    } as React.CSSProperties,
    textBox: {
        flex: 1,
        padding: '15px',
        fontSize: '16px',
        color: '#ffffff',
        backgroundColor: '#333',
        border: 'none',
        borderRadius: '15px',
        outline: 'none',
        resize: 'none',
        boxSizing: 'border-box',
        fontFamily: 'inherit',
    } as React.CSSProperties,
    button: {
        marginLeft: '10px',
        padding: '10px 20px',
        fontSize: '16px',
        backgroundColor: '#333',
        color: '#fff',
        border: '1px solid #ffffff',
        borderRadius: '15px',
        cursor: 'pointer',
        fontFamily: 'inherit',
    } as React.CSSProperties,
};

export default App;