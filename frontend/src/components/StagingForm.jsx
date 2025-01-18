import React, { useState } from 'react';
import axios from 'axios';

const StagingForm = () => {
    const [method, setMethod] = useState('');
    const [username, setUsername] = useState('');
    const [localPath, setLocalPath] = useState('');
    const [relativePath, setRelativePath] = useState('');
    const [response, setResponse] = useState(null);

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
            <h2>Staging Form</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Method" value={method} onChange={(e) => setMethod(e.target.value)} />
                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <input type="text" placeholder="Local Path" value={localPath} onChange={(e) => setLocalPath(e.target.value)} />
                <input type="text" placeholder="Relative Path" value={relativePath} onChange={(e) => setRelativePath(e.target.value)} />
                <button type="submit">Submit</button>
            </form>
            {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
        </div>
    );
};

export default StagingForm;
