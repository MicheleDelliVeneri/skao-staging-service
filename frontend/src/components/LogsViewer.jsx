import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/LogsViewer.css'; // Import the CSS file

const LogsViewer = () => {
    const [logs, setLogs] = useState('');

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const res = await axios.get('/logs/');
                setLogs(res.data);
            } catch {
                setLogs('Failed to fetch logs');
            }
        };

        fetchLogs();
        const interval = setInterval(fetchLogs, 5000); // Refresh every 5 seconds
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="logs-viewer">
            <h2>Logs</h2>
            <pre>{logs}</pre>
        </div>
    );
};

export default LogsViewer;