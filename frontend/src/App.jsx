import React from 'react';
import StagingForm from './components/StagingForm';
import LogsViewer from './components/LogsViewer';
import FileCreator from "./components/FileCreator";
import './styles/StagingForm.css'; // Include CSS for the whole app

const App = () => (
    <div>
        <header className="title-header">
            <h1>SKAO Staging Service</h1>
        </header>
        <div className="container">
            <FileCreator />
        </div>
        <div className="divider"></div>
        <div className="container">
            <StagingForm />
        </div>
        <div className="divider"></div>
        <div className="container">
            <LogsViewer />
        </div>
    </div>
);

export default App;