import React from 'react';
import StagingForm from './components/StagingForm';
import LogsViewer from './components/LogsViewer';
import FileCreator from "./components/FileCreator";
import './styles/StagingForm.css'; // Include CSS for the whole app
import './styles/App.css';

const App = () => (
    <div className="app-container">
        {/* Header with title and image */}
        <header className="app-header">
            <img src="/skao_logo.jpg" alt="SKAO Logo" className="header-logo"/>
            <h1 className="app-title">SKA Staging Service</h1>
        </header>
        {/* Grid Layout */}
        <div className="grid-container">
            <div className="grid-item">
                <FileCreator/>
            </div>
            <div className="grid-item">
                <StagingForm />
            </div>
            <div className="grid-item logs">
                <LogsViewer />
            </div>
        </div>

        {/* Footer with image */}
        <footer className="app-footer">
            <img src="/skao_logo.jpg" alt="SKAO Footer Logo" className="footer-logo" />
        </footer>
    </div>
);

export default App;
