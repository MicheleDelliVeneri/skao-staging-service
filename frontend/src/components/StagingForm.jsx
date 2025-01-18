import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/StagingForm.css'; // Import CSS file

const StagingForm = () => {
    const [methods, setMethods] = useState([]); // Store allowed methods
    const [method, setMethod] = useState('');
    const [username, setUsername] = useState('');
    const [localPath, setLocalPath] = useState('');
    const [relativePath, setRelativePath] = useState('');
    const [response, setResponse] = useState(null);

    // Fetch allowed methods from the backend
    useEffect(() => {
        const fetchMethods = async () => {
            try {
                const res = await axios.get('/config/allowed-methods/');
                if (res.data && Array.isArray(res.data.allowed_methods)) {
                    setMethods(res.data.allowed_methods); // Populate methods dropdown
                } else {
                    console.error('Invalid response structure:', res.data);
                }
            } catch (error) {
                console.error('Failed to fetch allowed methods:', error);
            }
        };
        fetchMethods(); // Call the fetch function
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post(`/stage-data/?method=${method}&username=${username}`, {
                data: { local_path_on_storage: localPath, relative_path: relativePath },
            });
            setResponse(res.data);
        } catch (error) {
            setResponse(error.response?.data || { detail: 'An error occurred' });
        }
    };

    return (
        <div>
            <header>
                <img src="./skao_logo.jpg" alt="Header" />
            </header>

            <div>
                <h2>Staging Form</h2>
                <form onSubmit={handleSubmit}>
                    <label htmlFor="method">Method</label>
                    <select
                        id="method"
                        value={method}
                        onChange={(e) => setMethod(e.target.value)}
                        required
                    >
                        <option value="" disabled>
                            Select a Method
                        </option>
                        {methods.map((m) => (
                            <option key={m} value={m}>
                                {m}
                            </option>
                        ))}
                    </select>

                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />

                    <label htmlFor="localPath">Local Path</label>
                    <input
                        type="text"
                        id="localPath"
                        placeholder="Local Path"
                        value={localPath}
                        onChange={(e) => setLocalPath(e.target.value)}
                        required
                    />

                    <label htmlFor="relativePath">Relative Path</label>
                    <input
                        type="text"
                        id="relativePath"
                        placeholder="Relative Path"
                        value={relativePath}
                        onChange={(e) => setRelativePath(e.target.value)}
                        required
                    />

                    <button type="submit">Submit</button>
                </form>

                {response && (
                    <div>
                        <h3>Response</h3>
                        <pre>{JSON.stringify(response, null, 2)}</pre>
                    </div>
                )}
            </div>

            <footer>
                <img src="skao_logo.jpg" alt="Footer" />
            </footer>
        </div>
    );
};

export default StagingForm;
