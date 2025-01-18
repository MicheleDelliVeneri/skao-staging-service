import React, { useState } from 'react';
import axios from 'axios';
import '../styles/FileCreator.css'; // Import the CSS file

const FileCreator = () => {
    const [filename, setFilename] = useState('');
    const [content, setContent] = useState('');
    const [response, setResponse] = useState(null);

    const handleCreateFile = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('/create-file/', {
                filename,
                content,
            });
            setResponse(res.data);
        } catch (error) {
            setResponse(error.response?.data || { detail: 'An error occurred' });
        }
    };

    return (
        <div className="file-creator">
            <h3>Create a File</h3>
            <form onSubmit={handleCreateFile}>
                <label htmlFor="filename">Filename</label>
                <input
                    type="text"
                    id="filename"
                    placeholder="Enter filename"
                    value={filename}
                    onChange={(e) => setFilename(e.target.value)}
                    required
                />

                <label htmlFor="content">Content</label>
                <textarea
                    id="content"
                    placeholder="Enter file content"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    required
                    rows="4"
                ></textarea>

                <button type="submit">Create File</button>
            </form>

            {response && (
                <div>
                    <h4>Response</h4>
                    <pre>{JSON.stringify(response, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default FileCreator;
