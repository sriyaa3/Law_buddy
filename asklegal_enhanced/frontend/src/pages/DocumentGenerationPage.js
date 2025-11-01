import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FaFileContract, FaDownload, FaCheckCircle } from 'react-icons/fa';
import { documentGenerationApi } from '../services/api';

const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageTitle = styled.h1`
  color: #2c3e50;
  margin-bottom: 20px;
`;

const TemplateGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const TemplateCard = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  cursor: pointer;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-3px);
  }
`;

const TemplateIcon = styled.div`
  font-size: 32px;
  color: #3498db;
  margin-bottom: 15px;
`;

const TemplateTitle = styled.h3`
  color: #2c3e50;
  margin: 0 0 10px;
`;

const TemplateDescription = styled.p`
  color: #7f8c8d;
  font-size: 14px;
  margin: 0 0 15px;
`;

const TemplateCategory = styled.span`
  background: #e8f4fc;
  color: #3498db;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
`;

const FormSection = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 30px;
`;

const FormTitle = styled.h2`
  color: #2c3e50;
  margin-top: 0;
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #2c3e50;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  
  &:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-height: 100px;
  
  &:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }
`;

const GenerateButton = styled.button`
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 30px;
  cursor: pointer;
  font-weight: 500;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  
  &:hover {
    background: #2980b9;
  }
  
  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
  }
`;

const ResultSection = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  text-align: center;
`;

const ResultIcon = styled.div`
  font-size: 48px;
  color: #27ae60;
  margin-bottom: 20px;
`;

const ResultTitle = styled.h2`
  color: #2c3e50;
  margin: 0 0 15px;
`;

const ResultMessage = styled.p`
  color: #7f8c8d;
  font-size: 16px;
  margin: 0 0 20px;
`;

const DownloadButton = styled.button`
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 25px;
  cursor: pointer;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  
  &:hover {
    background: #219653;
  }
  
  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
  }
`;

function DocumentGenerationPage() {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedDocument, setGeneratedDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isDownloading, setIsDownloading] = useState(false);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      const response = await documentGenerationApi.getTemplates();
      // Convert API response to component format
      const templateList = Object.entries(response.data.templates).map(([id, template]) => ({
        id,
        title: template.title,
        description: template.description,
        category: 'Legal Document',
        icon: <FaFileContract />,
        fields: template.fields.map(field => ({
          name: field,
          label: field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
          type: field.includes('address') ? 'textarea' : field.includes('date') ? 'date' : 'text'
        }))
      }));
      setTemplates(templateList);
    } catch (err) {
      console.error('Error fetching templates:', err);
      setError('Failed to load document templates');
    } finally {
      setLoading(false);
    }
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    // Initialize form data with empty values
    const initialData = {};
    template.fields.forEach(field => {
      initialData[field.name] = '';
    });
    setFormData(initialData);
    setGeneratedDocument(null);
  };

  const handleInputChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  const handleGenerateDocument = async () => {
    if (!selectedTemplate) return;
    
    setIsGenerating(true);
    setError(null);
    
    try {
      // Prepare the request data
      const documentRequest = {
        template_type: selectedTemplate.id,
        details: formData
      };
      
      // Call the document generation API
      const response = await documentGenerationApi.generateDocument(documentRequest);
      
      setGeneratedDocument(response.data);
    } catch (error) {
      console.error('Error generating document:', error);
      setError('Error generating document. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownloadDocument = async () => {
    if (!generatedDocument) return;
    
    setIsDownloading(true);
    try {
      // Use the API service to download the document
      const response = await documentGenerationApi.downloadDocument(generatedDocument.document_id);
      
      // Create a blob from the response data
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      });
      
      // Create a temporary URL for the blob
      const url = window.URL.createObjectURL(blob);
      
      // Create a temporary anchor element and trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = generatedDocument.filename;
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Error downloading document:', error);
      // Fallback: try direct download
      try {
        const downloadUrl = `${window.location.origin}/api/v1/document-generation/generated/${generatedDocument.document_id}`;
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = generatedDocument.filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (fallbackError) {
        console.error('Fallback download also failed:', fallbackError);
        setError('Error downloading document. Please try again.');
      }
    } finally {
      setIsDownloading(false);
    }
  };

  if (loading) {
    return (
      <PageContainer>
        <PageTitle>Document Generation</PageTitle>
        <p>Loading templates...</p>
      </PageContainer>
    );
  }

  if (error && !selectedTemplate) {
    return (
      <PageContainer>
        <PageTitle>Document Generation</PageTitle>
        <p>Error: {error}</p>
        <button onClick={fetchTemplates}>Retry</button>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <PageTitle>Document Generation</PageTitle>
      
      {!selectedTemplate && !generatedDocument && (
        <>
          <p>Select a document template to get started:</p>
          <TemplateGrid>
            {templates.map((template) => (
              <TemplateCard 
                key={template.id} 
                onClick={() => handleTemplateSelect(template)}
              >
                <TemplateIcon>
                  {template.icon}
                </TemplateIcon>
                <TemplateTitle>{template.title}</TemplateTitle>
                <TemplateDescription>{template.description}</TemplateDescription>
                <TemplateCategory>{template.category}</TemplateCategory>
              </TemplateCard>
            ))}
          </TemplateGrid>
        </>
      )}
      
      {selectedTemplate && !generatedDocument && (
        <FormSection>
          <FormTitle>Generate {selectedTemplate.title}</FormTitle>
          <p>Please fill in the details below:</p>
          
          {selectedTemplate.fields.map((field) => (
            <FormGroup key={field.name}>
              <Label htmlFor={field.name}>{field.label}</Label>
              {field.type === 'textarea' ? (
                <TextArea
                  id={field.name}
                  value={formData[field.name] || ''}
                  onChange={(e) => handleInputChange(field.name, e.target.value)}
                  placeholder={field.placeholder || ''}
                />
              ) : (
                <Input
                  id={field.name}
                  type={field.type}
                  value={formData[field.name] || ''}
                  onChange={(e) => handleInputChange(field.name, e.target.value)}
                  placeholder={field.placeholder || ''}
                />
              )}
            </FormGroup>
          ))}
          
          {error && <p style={{color: 'red'}}>{error}</p>}
          
          <GenerateButton 
            onClick={handleGenerateDocument} 
            disabled={isGenerating}
          >
            {isGenerating ? 'Generating...' : 'Generate Document'}
          </GenerateButton>
        </FormSection>
      )}
      
      {generatedDocument && (
        <ResultSection>
          <ResultIcon>
            <FaCheckCircle />
          </ResultIcon>
          <ResultTitle>Document Generated Successfully!</ResultTitle>
          <ResultMessage>
            Your {selectedTemplate?.title} has been created and is ready for download.
          </ResultMessage>
          <DownloadButton 
            onClick={handleDownloadDocument}
            disabled={isDownloading}
          >
            <FaDownload /> {isDownloading ? 'Downloading...' : 'Download Document'}
          </DownloadButton>
        </ResultSection>
      )}
    </PageContainer>
  );
}

export default DocumentGenerationPage;