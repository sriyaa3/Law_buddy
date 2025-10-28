import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatPage from './pages/ChatPage';
import DocumentPage from './pages/DocumentPage';
import DocumentGenerationPage from './pages/DocumentGenerationPage';
import CompliancePage from './pages/CompliancePage';
import WorkflowPage from './pages/WorkflowPage';
import ProfilePage from './pages/ProfilePage';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f7fa;
`;

const MainContent = styled.div`
  display: flex;
  flex: 1;
  overflow: hidden;
`;

const ContentArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
`;

function App() {
  return (
    <Router>
      <AppContainer>
        <Header />
        <MainContent>
          <Sidebar />
          <ContentArea>
            <Routes>
              <Route path="/" element={<ChatPage />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/documents" element={<DocumentPage />} />
              <Route path="/document-generation" element={<DocumentGenerationPage />} />
              <Route path="/compliance" element={<CompliancePage />} />
              <Route path="/workflows" element={<WorkflowPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </ContentArea>
        </MainContent>
      </AppContainer>
    </Router>
  );
}

export default App;