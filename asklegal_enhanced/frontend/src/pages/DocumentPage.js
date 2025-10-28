import React, { useState } from 'react';
import styled from 'styled-components';
import { 
  FaUpload, 
  FaFilePdf, 
  FaFileWord, 
  FaFileAlt, 
  FaSearch, 
  FaChartBar,
  FaGavel,
  FaFileContract,
  FaDownload
} from 'react-icons/fa';
import { documentApi } from '../services/api';

const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageTitle = styled.h1`
  color: #2c3e50;
  margin-bottom: 20px;
`;

const Tabs = styled.div`
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
`;

const Tab = styled.div`
  padding: 12px 20px;
  cursor: pointer;
  border-bottom: 3px solid ${props => props.active ? '#3498db' : 'transparent'};
  color: ${props => props.active ? '#3498db' : '#7f8c8d'};
  font-weight: 500;
  
  &:hover {
    color: #3498db;
  }
`;

const UploadSection = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 30px;
  text-align: center;
`;

const UploadArea = styled.div`
  border: 2px dashed #3498db;
  border-radius: 8px;
  padding: 40px 20px;
  margin: 20px 0;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background-color: #f8f9fa;
  }
`;

const UploadIcon = styled.div`
  font-size: 48px;
  color: #3498db;
  margin-bottom: 15px;
`;

const UploadText = styled.div`
  font-size: 18px;
  color: #7f8c8d;
  margin-bottom: 10px;
`;

const UploadHint = styled.div`
  font-size: 14px;
  color: #95a5a6;
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const FeatureCard = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-3px);
  }
`;

const FeatureIcon = styled.div`
  font-size: 32px;
  color: #3498db;
  margin-bottom: 15px;
`;

const FeatureTitle = styled.h3`
  color: #2c3e50;
  margin: 0 0 10px;
`;

const FeatureDescription = styled.p`
  color: #7f8c8d;
  font-size: 14px;
  margin: 0;
`;

const FileList = styled.div`
  margin-top: 30px;
`;

const FileItem = styled.div`
  display: flex;
  align-items: center;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 10px;
  background: white;
`;

const FileIcon = styled.div`
  font-size: 24px;
  color: #3498db;
  margin-right: 15px;
`;

const FileInfo = styled.div`
  flex: 1;
`;

const FileName = styled.div`
  font-weight: 500;
  margin-bottom: 5px;
`;

const FileMeta = styled.div`
  font-size: 14px;
  color: #7f8c8d;
`;

const StatusBadge = styled.span`
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  
  ${props => props.status === 'uploaded' && `
    background-color: #e8f4fc;
    color: #3498db;
  `}
  
  ${props => props.status === 'processing' && `
    background-color: #fef9e7;
    color: #f39c12;
  `}
  
  ${props => props.status === 'completed' && `
    background-color: #eafaf1;
    color: #27ae60;
  `}
  
  ${props => props.status === 'analyzed' && `
    background-color: #eafaf1;
    color: #27ae60;
  `}
  
  ${props => props.status === 'error' && `
    background-color: #fadbd8;
    color: #e74c3c;
  `}
`;

const ActionButton = styled.button`
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-left: 10px;
  
  &:hover {
    background: #2980b9;
  }
  
  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
  }
`;

const AnalysisSection = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-top: 20px;
`;

const AnalysisTitle = styled.h3`
  color: #2c3e50;
  margin-top: 0;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const AnalysisItem = styled.div`
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
  
  &:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }
`;

const AnalysisLabel = styled.div`
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 5px;
`;

const AnalysisValue = styled.div`
  color: #7f8c8d;
  font-size: 14px;
`;

const ClauseList = styled.ul`
  margin: 0;
  padding-left: 20px;
`;

const ClauseItem = styled.li`
  margin-bottom: 5px;
`;

const RecommendationList = styled.ul`
  margin: 0;
  padding-left: 20px;
`;

const RecommendationItem = styled.li`
  margin-bottom: 5px;
`;

function DocumentPage() {
  const [files, setFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [activeTab, setActiveTab] = useState('upload');
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [error, setError] = useState(null);
  
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setIsUploading(true);
    setError(null);
    
    try {
      // Add file to list with uploading status
      const newFile = {
        id: Date.now(),
        name: file.name,
        size: file.size,
        type: file.type,
        status: 'uploading',
        uploadedAt: new Date()
      };
      
      setFiles(prev => [...prev, newFile]);
      
      // Upload to backend
      const response = await documentApi.uploadDocument(file);
      
      // Update file with response data
      const uploadedFile = {
        ...newFile,
        status: 'uploaded',
        ...response.data
      };
      
      setFiles(prev => prev.map(f => 
        f.id === newFile.id ? uploadedFile : f
      ));
      
      // Set as selected file for analysis display
      setSelectedFile(uploadedFile);
      
    } catch (error) {
      console.error('Error uploading file:', error);
      // Update file status to error
      setFiles(prev => prev.map(f => 
        f.id === newFile.id 
          ? { ...f, status: 'error' } 
          : f
      ));
      setError('Error uploading file. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };
  
  const getFileIcon = (fileType) => {
    if (fileType.includes('pdf')) return <FaFilePdf />;
    if (fileType.includes('word') || fileType.includes('document')) return <FaFileWord />;
    return <FaFileAlt />;
  };
  
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };
  
  const handleAnalyzeDocument = async (documentId) => {
    try {
      // Set loading state
      setFiles(prev => prev.map(f => 
        f.document_id === documentId 
          ? { ...f, status: 'processing' } 
          : f
      ));
      
      // In a real implementation, we would call a specific analysis endpoint
      // For now, we'll simulate by using the existing document data
      const file = files.find(f => f.document_id === documentId);
      if (file) {
        setAnalysisResult({
          document_id: documentId,
          filename: file.name,
          document_type: file.document_type,
          summary: file.summary,
          key_points: file.key_points,
          legal_clauses: ["Confidentiality Clause", "Termination Clause", "Payment Terms", "Dispute Resolution"],
          compliance_issues: ["Review payment terms for compliance", "Verify termination notice period"],
          recommendations: [
            "Ensure all parties have signed the document",
            "Keep a copy for your records",
            "Review terms periodically"
          ]
        });
        
        // Update file status
        setFiles(prev => prev.map(f => 
          f.document_id === documentId 
            ? { ...f, status: 'analyzed' } 
            : f
        ));
      }
    } catch (error) {
      console.error('Error analyzing document:', error);
      setError('Error analyzing document. Please try again.');
      // Update file status to error
      setFiles(prev => prev.map(f => 
        f.document_id === documentId 
          ? { ...f, status: 'error' } 
          : f
      ));
    }
  };
  
  const handlePredictOutcome = async (documentId) => {
    try {
      // Set loading state
      setFiles(prev => prev.map(f => 
        f.document_id === documentId 
          ? { ...f, status: 'processing' } 
          : f
      ));
      
      // Simulate judgment prediction
      const prediction = {
        case_id: "case_" + documentId.substring(0, 6),
        predicted_verdict: Math.random() > 0.5 ? "Favorable" : "Unfavorable",
        confidence_score: Math.random() * 0.4 + 0.6, // 0.6 to 1.0
        key_factors: [
          "Evidence strength",
          "Legal precedent",
          "Contract terms",
          "Witness credibility"
        ],
        legal_reasoning: "Based on the document analysis and relevant laws, the prediction considers factors such as evidence strength, legal precedents, and applicable statutes.",
        recommended_actions: [
          "Gather additional supporting evidence",
          "Consult with specialized legal counsel",
          "Review relevant case precedents",
          "Prepare counter-arguments for weak points"
        ]
      };
      
      setPredictionResult(prediction);
      
      // Update file status
      setFiles(prev => prev.map(f => 
        f.document_id === documentId 
          ? { ...f, status: 'analyzed' } 
          : f
      ));
    } catch (error) {
      console.error('Error predicting outcome:', error);
      setError('Error predicting outcome. Please try again.');
      // Update file status to error
      setFiles(prev => prev.map(f => 
        f.document_id === documentId 
          ? { ...f, status: 'error' } 
          : f
      ));
    }
  };
  
  const handleDownloadDocument = (filename) => {
    // In a real implementation, this would download the document
    alert(`In a full implementation, this would download: ${filename}`);
  };
  
  return (
    <PageContainer>
      <PageTitle>Document Processing & Legal Analysis</PageTitle>
      
      {error && (
        <div style={{backgroundColor: '#fadbd8', color: '#e74c3c', padding: '10px', borderRadius: '4px', marginBottom: '20px'}}>
          {error}
        </div>
      )}
      
      <Tabs>
        <Tab active={activeTab === 'upload'} onClick={() => setActiveTab('upload')}>
          Upload Documents
        </Tab>
        <Tab active={activeTab === 'features'} onClick={() => setActiveTab('features')}>
          Features
        </Tab>
      </Tabs>
      
      {activeTab === 'upload' ? (
        <>
          <UploadSection>
            <UploadIcon>
              <FaUpload />
            </UploadIcon>
            <UploadText>Upload Legal Documents</UploadText>
            <UploadHint>Supports PDF, DOCX, and TXT files up to 10MB</UploadHint>
            
            <UploadArea onClick={() => document.getElementById('fileInput').click()}>
              <input
                id="fileInput"
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
                disabled={isUploading}
              />
              <ActionButton disabled={isUploading}>
                {isUploading ? 'Uploading...' : 'Select Files'}
              </ActionButton>
            </UploadArea>
          </UploadSection>
          
          {files.length > 0 && (
            <FileList>
              <h3>Uploaded Documents</h3>
              {files.map((file) => (
                <FileItem key={file.id}>
                  <FileIcon>
                    {getFileIcon(file.type)}
                  </FileIcon>
                  <FileInfo>
                    <FileName>{file.name}</FileName>
                    <FileMeta>
                      {formatFileSize(file.size)} • Uploaded {file.uploadedAt.toLocaleDateString()}
                    </FileMeta>
                    {file.document_type && (
                      <FileMeta>
                        Document Type: {file.document_type}
                      </FileMeta>
                    )}
                  </FileInfo>
                  <StatusBadge status={file.status}>
                    {file.status.charAt(0).toUpperCase() + file.status.slice(1)}
                  </StatusBadge>
                  <ActionButton 
                    onClick={() => handleAnalyzeDocument(file.document_id)}
                    disabled={file.status !== 'uploaded' && file.status !== 'analyzed'}
                  >
                    <FaSearch /> Analyze
                  </ActionButton>
                  <ActionButton 
                    onClick={() => handlePredictOutcome(file.document_id)}
                    disabled={file.status !== 'uploaded' && file.status !== 'analyzed'}
                  >
                    <FaGavel /> Predict
                  </ActionButton>
                  <ActionButton 
                    onClick={() => handleDownloadDocument(file.filename)}
                    disabled={file.status === 'uploading' || file.status === 'error'}
                  >
                    <FaDownload /> Download
                  </ActionButton>
                </FileItem>
              ))}
            </FileList>
          )}
          
          {analysisResult && (
            <AnalysisSection>
              <AnalysisTitle>
                <FaSearch /> Document Analysis: {analysisResult.filename}
              </AnalysisTitle>
              <AnalysisItem>
                <AnalysisLabel>Document Type</AnalysisLabel>
                <AnalysisValue>{analysisResult.document_type || 'Unknown'}</AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Summary</AnalysisLabel>
                <AnalysisValue>{analysisResult.summary || 'No summary available'}</AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Key Points</AnalysisLabel>
                <AnalysisValue>
                  {analysisResult.key_points && analysisResult.key_points.length > 0 
                    ? analysisResult.key_points.join(', ') 
                    : 'No key points identified'}
                </AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Legal Clauses Identified</AnalysisLabel>
                <AnalysisValue>
                  {analysisResult.legal_clauses && analysisResult.legal_clauses.length > 0 ? (
                    <ClauseList>
                      {analysisResult.legal_clauses.map((clause, index) => (
                        <ClauseItem key={index}>{clause}</ClauseItem>
                      ))}
                    </ClauseList>
                  ) : (
                    'No specific clauses identified'
                  )}
                </AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Compliance Issues</AnalysisLabel>
                <AnalysisValue>
                  {analysisResult.compliance_issues && analysisResult.compliance_issues.length > 0 ? (
                    <ClauseList>
                      {analysisResult.compliance_issues.map((issue, index) => (
                        <ClauseItem key={index}>{issue}</ClauseItem>
                      ))}
                    </ClauseList>
                  ) : (
                    'No compliance issues identified'
                  )}
                </AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Recommendations</AnalysisLabel>
                <AnalysisValue>
                  {analysisResult.recommendations && analysisResult.recommendations.length > 0 ? (
                    <RecommendationList>
                      {analysisResult.recommendations.map((recommendation, index) => (
                        <RecommendationItem key={index}>{recommendation}</RecommendationItem>
                      ))}
                    </RecommendationList>
                  ) : (
                    'No recommendations available'
                  )}
                </AnalysisValue>
              </AnalysisItem>
            </AnalysisSection>
          )}
          
          {predictionResult && (
            <AnalysisSection>
              <AnalysisTitle>
                <FaGavel /> Judgment Prediction: {predictionResult.case_id}
              </AnalysisTitle>
              <AnalysisItem>
                <AnalysisLabel>Predicted Verdict</AnalysisLabel>
                <AnalysisValue>
                  <StatusBadge status={predictionResult.predicted_verdict === 'Favorable' ? 'completed' : 'error'}>
                    {predictionResult.predicted_verdict}
                  </StatusBadge>
                </AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Confidence Score</AnalysisLabel>
                <AnalysisValue>
                  {(predictionResult.confidence_score * 100).toFixed(1)}%
                </AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Key Factors</AnalysisLabel>
                <AnalysisValue>
                  {predictionResult.key_factors && predictionResult.key_factors.length > 0 ? (
                    <ClauseList>
                      {predictionResult.key_factors.map((factor, index) => (
                        <ClauseItem key={index}>{factor}</ClauseItem>
                      ))}
                    </ClauseList>
                  ) : (
                    'No key factors identified'
                  )}
                </AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Legal Reasoning</AnalysisLabel>
                <AnalysisValue>{predictionResult.legal_reasoning}</AnalysisValue>
              </AnalysisItem>
              <AnalysisItem>
                <AnalysisLabel>Recommended Actions</AnalysisLabel>
                <AnalysisValue>
                  {predictionResult.recommended_actions && predictionResult.recommended_actions.length > 0 ? (
                    <RecommendationList>
                      {predictionResult.recommended_actions.map((action, index) => (
                        <RecommendationItem key={index}>{action}</RecommendationItem>
                      ))}
                    </RecommendationList>
                  ) : (
                    'No recommended actions'
                  )}
                </AnalysisValue>
              </AnalysisItem>
            </AnalysisSection>
          )}
        </>
      ) : (
        <FeaturesGrid>
          <FeatureCard>
            <FeatureIcon>
              <FaFileContract />
            </FeatureIcon>
            <FeatureTitle>Document Analysis</FeatureTitle>
            <FeatureDescription>
              Upload contracts and legal documents for detailed analysis, clause identification, and risk assessment.
            </FeatureDescription>
          </FeatureCard>
          
          <FeatureCard>
            <FeatureIcon>
              <FaSearch />
            </FeatureIcon>
            <FeatureTitle>Legal Insights</FeatureTitle>
            <FeatureDescription>
              Extract key legal information, identify compliance issues, and get actionable recommendations.
            </FeatureDescription>
          </FeatureCard>
          
          <FeatureCard>
            <FeatureIcon>
              <FaGavel />
            </FeatureIcon>
            <FeatureTitle>Judgment Prediction</FeatureTitle>
            <FeatureDescription>
              Analyze case documents to predict legal outcomes and assess success probabilities.
            </FeatureDescription>
          </FeatureCard>
          
          <FeatureCard>
            <FeatureIcon>
              <FaChartBar />
            </FeatureIcon>
            <FeatureTitle>Risk Assessment</FeatureTitle>
            <FeatureDescription>
              Identify potential legal risks and get mitigation strategies for your business documents.
            </FeatureDescription>
          </FeatureCard>
        </FeaturesGrid>
      )}
    </PageContainer>
  );
}

export default DocumentPage;