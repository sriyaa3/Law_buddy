import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FaClipboardCheck, FaExclamationTriangle, FaCheckCircle, FaClock } from 'react-icons/fa';
import { msmeApi } from '../services/api';

const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageTitle = styled.h1`
  color: #2c3e50;
  margin-bottom: 20px;
`;

const DashboardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const StatCard = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
`;

const StatIcon = styled.div`
  font-size: 32px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  
  ${props => props.color === 'blue' && `
    background-color: #e8f4fc;
    color: #3498db;
  `}
  
  ${props => props.color === 'green' && `
    background-color: #eafaf1;
    color: #27ae60;
  `}
  
  ${props => props.color === 'orange' && `
    background-color: #fef9e7;
    color: #f39c12;
  `}
  
  ${props => props.color === 'red' && `
    background-color: #fdedec;
    color: #e74c3c;
  `}
`;

const StatInfo = styled.div`
  flex: 1;
`;

const StatNumber = styled.div`
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
`;

const StatLabel = styled.div`
  font-size: 14px;
  color: #7f8c8d;
`;

const SectionTitle = styled.h2`
  color: #2c3e50;
  margin: 30px 0 20px;
`;

const Checklist = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const ChecklistItem = styled.div`
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  
  &:last-child {
    border-bottom: none;
  }
  
  ${props => props.completed && `
    background-color: #f8f9fa;
  `}
`;

const ItemCheckbox = styled.input`
  margin-right: 15px;
  width: 18px;
  height: 18px;
`;

const ItemContent = styled.div`
  flex: 1;
`;

const ItemTitle = styled.div`
  font-weight: 500;
  margin-bottom: 5px;
  ${props => props.completed && `
    color: #95a5a6;
    text-decoration: line-through;
  `}
`;

const ItemDescription = styled.div`
  font-size: 14px;
  color: #7f8c8d;
`;

const ItemDueDate = styled.div`
  font-size: 12px;
  color: #95a5a6;
  display: flex;
  align-items: center;
  gap: 5px;
`;

const PriorityBadge = styled.span`
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  margin-left: 10px;
  
  ${props => props.priority === 'high' && `
    background-color: #fdedec;
    color: #e74c3c;
  `}
  
  ${props => props.priority === 'medium' && `
    background-color: #fef9e7;
    color: #f39c12;
  `}
  
  ${props => props.priority === 'low' && `
    background-color: #e8f4fc;
    color: #3498db;
  `}
`;

function CompliancePage() {
  const [complianceItems, setComplianceItems] = useState([
    {
      id: 1,
      title: "Register for GST",
      description: "Complete GST registration for your business",
      dueDate: "2025-11-15",
      priority: "high",
      completed: false
    },
    {
      id: 2,
      title: "File Annual Returns",
      description: "Submit annual returns to the Registrar of Companies",
      dueDate: "2025-12-31",
      priority: "high",
      completed: false
    },
    {
      id: 3,
      title: "Renew Shop License",
      description: "Renew your shop and establishment license",
      dueDate: "2025-11-30",
      priority: "medium",
      completed: true
    },
    {
      id: 4,
      title: "Update Employee Records",
      description: "Maintain updated records for all employees",
      dueDate: "2025-10-31",
      priority: "medium",
      completed: false
    }
  ]);
  
  const toggleItemCompletion = (id) => {
    setComplianceItems(prev => 
      prev.map(item => 
        item.id === id 
          ? { ...item, completed: !item.completed } 
          : item
      )
    );
  };
  
  const completedCount = complianceItems.filter(item => item.completed).length;
  const totalCount = complianceItems.length;
  const pendingCount = totalCount - completedCount;
  const highPriorityCount = complianceItems.filter(item => item.priority === 'high' && !item.completed).length;
  
  return (
    <PageContainer>
      <PageTitle>Compliance Dashboard</PageTitle>
      
      <DashboardGrid>
        <StatCard>
          <StatIcon color="blue">
            <FaClipboardCheck />
          </StatIcon>
          <StatInfo>
            <StatNumber>{totalCount}</StatNumber>
            <StatLabel>Total Requirements</StatLabel>
          </StatInfo>
        </StatCard>
        
        <StatCard>
          <StatIcon color="green">
            <FaCheckCircle />
          </StatIcon>
          <StatInfo>
            <StatNumber>{completedCount}</StatNumber>
            <StatLabel>Completed</StatLabel>
          </StatInfo>
        </StatCard>
        
        <StatCard>
          <StatIcon color="orange">
            <FaClock />
          </StatIcon>
          <StatInfo>
            <StatNumber>{pendingCount}</StatNumber>
            <StatLabel>Pending</StatLabel>
          </StatInfo>
        </StatCard>
        
        <StatCard>
          <StatIcon color="red">
            <FaExclamationTriangle />
          </StatIcon>
          <StatInfo>
            <StatNumber>{highPriorityCount}</StatNumber>
            <StatLabel>High Priority</StatLabel>
          </StatInfo>
        </StatCard>
      </DashboardGrid>
      
      <SectionTitle>Compliance Checklist</SectionTitle>
      
      <Checklist>
        {complianceItems.map((item) => (
          <ChecklistItem key={item.id} completed={item.completed}>
            <ItemCheckbox
              type="checkbox"
              checked={item.completed}
              onChange={() => toggleItemCompletion(item.id)}
            />
            <ItemContent>
              <ItemTitle completed={item.completed}>
                {item.title}
                <PriorityBadge priority={item.priority}>
                  {item.priority.toUpperCase()}
                </PriorityBadge>
              </ItemTitle>
              <ItemDescription>{item.description}</ItemDescription>
            </ItemContent>
            <ItemDueDate>
              <FaClock /> Due: {item.dueDate}
            </ItemDueDate>
          </ChecklistItem>
        ))}
      </Checklist>
    </PageContainer>
  );
}

export default CompliancePage;