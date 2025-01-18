import React from 'react';
import StagingForm from './components/StagingForm';
import LogsViewer from './components/LogsViewer';

const App = () => (
    <div>
        <h1>SKAO Staging Service</h1>
        <StagingForm />
        <LogsViewer />
    </div>
);

export default App;
