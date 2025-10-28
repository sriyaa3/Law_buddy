import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FaTasks, FaPlus, FaPlay, FaCheck, FaEllipsisH } from 'react-icons/fa';
import { msmeApi } from '../services/api';

const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageTitle = styled.h1`
  color: #2c3e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const CreateButton = styled.button`
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  
  &:hover {
    background: #2980b9;
  }
`;

const WorkflowGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
`;

const WorkflowCard = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
  }
`;

const CardHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid #eee;
  background-color: #f8f9fa;
`;

const CardTitle = styled.h3`
  margin: 0 0 5px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const CardDescription = styled.p`
  margin: 0;
  color: #7f8c8d;
  font-size: 14px;
`;

const ProgressBar = styled.div`
  height: 6px;
  background-color: #ecf0f1;
  border-radius: 3px;
  margin: 15px 0;
  overflow: hidden;
`;

const ProgressFill = styled.div`
  height: 100%;
  background-color: #3498db;
  width: ${props => props.progress}%;
  transition: width 0.3s;
`;

const ProgressText = styled.div`
  font-size: 12px;
  color: #7f8c8d;
  display: flex;
  justify-content: space-between;
`;

const CardBody = styled.div`
  padding: 20px;
`;

const StepsList = styled.div`
  margin-bottom: 20px;
`;

const StepItem = styled.div`
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f1f2f6;
  
  &:last-child {
    border-bottom: none;
  }
`;

const StepNumber = styled.div`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: ${props => {
    if (props.status === 'completed') return '#27ae60';
    if (props.status === 'in_progress') return '#3498db';
    return '#bdc3c7';
  }};
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  margin-right: 12px;
`;

const StepContent = styled.div`
  flex: 1;
`;

const StepTitle = styled.div`
  font-weight: 500;
  margin-bottom: 3px;
  color: ${props => {
    if (props.status === 'completed') return '#27ae60';
    if (props.status === 'in_progress') return '#3498db';
    return '#2c3e50';
  }};
`;

const StepDescription = styled.div`
  font-size: 13px;
  color: #7f8c8d;
`;

const CardFooter = styled.div`
  padding: 15px 20px;
  background-color: #f8f9fa;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
`;

const ActionButton = styled.button`
  background: ${props => props.primary ? '#3498db' : '#ecf0f1'};
  color: ${props => props.primary ? 'white' : '#2c3e50'};
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  
  &:hover {
    background: ${props => props.primary ? '#2980b9' : '#d5dbdb'};
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: white;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
`;

const ModalHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const ModalTitle = styled.h2`
  margin: 0;
  color: #2c3e50;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #7f8c8d;
`;

const ModalBody = styled.div`
  padding: 20px;
`;

const FormGroup = styled.div`
  margin-bottom: 15px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #2c3e50;
`;

const Select = styled.select`
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
`;

const ModalFooter = styled.div`
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
`;

const CancelButton = styled.button`
  background: #ecf0f1;
  color: #2c3e50;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
  
  &:hover {
    background: #d5dbdb;
  }
`;

const CreateWorkflowButton = styled.button`
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
  
  &:hover {
    background: #2980b9;
  }
  
  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
  }
`;

function WorkflowPage() {
  const [workflows, setWorkflows] = useState([
    {
      id: 1,
      name: "Compliance Check",
      description: "Complete legal compliance requirements",
      progress: 75,
      totalSteps: 4,
      completedSteps: 3,
      steps: [
        { id: 1, title: "Review Legal Requirements", description: "Review industry-specific legal requirements", status: "completed" },
        { id: 2, title: "Gather Documentation", description: "Collect required documents and certificates", status: "completed" },
        { id: 3, title: "Submit Applications", description: "Submit applications to relevant authorities", status: "completed" },
        { id: 4, title: "Follow Up", description: "Follow up on pending applications", status: "in_progress" }
      ]
    },
    {
      id: 2,
      name: "Employee Onboarding",
      description: "Complete employee onboarding process",
      progress: 25,
      totalSteps: 4,
      completedSteps: 1,
      steps: [
        { id: 1, title: "Prepare Documentation", description: "Prepare employment contract and policies", status: "completed" },
        { id: 2, title: "Background Check", description: "Conduct background verification", status: "pending" },
        { id: 3, title: "Orientation", description: "Conduct employee orientation session", status: "pending" },
        { id: 4, title: "Training", description: "Provide role-specific training", status: "pending" }
      ]
    }
  ]);
  
  const [showModal, setShowModal] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  
  const workflowTemplates = [
    { id: 'compliance_check', name: 'Compliance Check', description: 'Complete legal compliance requirements' },
    { id: 'contract_management', name: 'Contract Management', description: 'Manage business contracts and agreements' },
    { id: 'employee_onboarding', name: 'Employee Onboarding', description: 'Complete employee onboarding process' }
  ];
  
  const handleCreateWorkflow = () => {
    if (!selectedTemplate) return;
    
    // In a real app, this would call the API
    const template = workflowTemplates.find(t => t.id === selectedTemplate);
    if (template) {
      const newWorkflow = {
        id: Date.now(),
        name: template.name,
        description: template.description,
        progress: 0,
        totalSteps: 4,
        completedSteps: 0,
        steps: [
          { id: 1, title: "Step 1", description: "First step description", status: "pending" },
          { id: 2, title: "Step 2", description: "Second step description", status: "pending" },
          { id: 3, title: "Step 3", description: "Third step description", status: "pending" },
          { id: 4, title: "Step 4", description: "Fourth step description", status: "pending" }
        ]
      };
      
      setWorkflows(prev => [...prev, newWorkflow]);
      setShowModal(false);
      setSelectedTemplate('');
    }
  };
  
  const startWorkflowStep = (workflowId, stepIndex) => {
    setWorkflows(prev => 
      prev.map(workflow => {
        if (workflow.id === workflowId) {
          const updatedSteps = [...workflow.steps];
          if (stepIndex < updatedSteps.length) {
            updatedSteps[stepIndex].status = 'in_progress';
          }
          return { ...workflow, steps: updatedSteps };
        }
        return workflow;
      })
    );
  };
  
  const completeWorkflowStep = (workflowId, stepIndex) => {
    setWorkflows(prev => 
      prev.map(workflow => {
        if (workflow.id === workflowId) {
          const updatedSteps = [...workflow.steps];
          if (stepIndex < updatedSteps.length) {
            updatedSteps[stepIndex].status = 'completed';
          }
          
          // Calculate progress
          const completedSteps = updatedSteps.filter(step => step.status === 'completed').length;
          const progress = Math.round((completedSteps / updatedSteps.length) * 100);
          
          return { 
            ...workflow, 
            steps: updatedSteps,
            completedSteps,
            progress
          };
        }
        return workflow;
      })
    );
  };
  
  return (
    <PageContainer>
      <PageTitle>
        Workflow Management
        <CreateButton onClick={() => setShowModal(true)}>
          <FaPlus /> Create Workflow
        </CreateButton>
      </PageTitle>
      
      <WorkflowGrid>
        {workflows.map((workflow) => (
          <WorkflowCard key={workflow.id}>
            <CardHeader>
              <CardTitle>
                <FaTasks /> {workflow.name}
              </CardTitle>
              <CardDescription>{workflow.description}</CardDescription>
              
              <ProgressBar progress={workflow.progress}>
                <ProgressFill progress={workflow.progress} />
              </ProgressBar>
              <ProgressText>
                <span>{workflow.completedSteps}/{workflow.totalSteps} steps completed</span>
                <span>{workflow.progress}%</span>
              </ProgressText>
            </CardHeader>
            
            <CardBody>
              <StepsList>
                {workflow.steps.map((step, index) => (
                  <StepItem key={step.id}>
                    <StepNumber status={step.status}>
                      {step.status === 'completed' ? <FaCheck /> : index + 1}
                    </StepNumber>
                    <StepContent>
                      <StepTitle status={step.status}>{step.title}</StepTitle>
                      <StepDescription>{step.description}</StepDescription>
                    </StepContent>
                  </StepItem>
                ))}
              </StepsList>
            </CardBody>
            
            <CardFooter>
              <ActionButton>
                <FaEllipsisH />
              </ActionButton>
              <ActionButton primary>
                <FaPlay /> Start Next Step
              </ActionButton>
            </CardFooter>
          </WorkflowCard>
        ))}
      </WorkflowGrid>
      
      {showModal && (
        <ModalOverlay>
          <ModalContent>
            <ModalHeader>
              <ModalTitle>Create New Workflow</ModalTitle>
              <CloseButton onClick={() => setShowModal(false)}>×</CloseButton>
            </ModalHeader>
            
            <ModalBody>
              <FormGroup>
                <Label>Select Workflow Template</Label>
                <Select 
                  value={selectedTemplate} 
                  onChange={(e) => setSelectedTemplate(e.target.value)}
                >
                  <option value="">Choose a template...</option>
                  {workflowTemplates.map((template) => (
                    <option key={template.id} value={template.id}>
                      {template.name} - {template.description}
                    </option>
                  ))}
                </Select>
              </FormGroup>
            </ModalBody>
            
            <ModalFooter>
              <CancelButton onClick={() => setShowModal(false)}>
                Cancel
              </CancelButton>
              <CreateWorkflowButton 
                onClick={handleCreateWorkflow}
                disabled={!selectedTemplate}
              >
                Create Workflow
              </CreateWorkflowButton>
            </ModalFooter>
          </ModalContent>
        </ModalOverlay>
      )}
    </PageContainer>
  );
}

export default WorkflowPage;