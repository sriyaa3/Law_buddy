import React, { useState } from 'react';
import styled from 'styled-components';
import { FaUser, FaBuilding, FaMapMarkerAlt, FaUsers, FaFileInvoice } from 'react-icons/fa';

const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageTitle = styled.h1`
  color: #2c3e50;
  margin-bottom: 20px;
`;

const ProfileGrid = styled.div`
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
`;

const ProfileSidebar = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 25px;
  height: fit-content;
`;

const Avatar = styled.div`
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  margin: 0 auto 20px;
`;

const UserName = styled.h2`
  text-align: center;
  color: #2c3e50;
  margin: 0 0 5px;
`;

const UserEmail = styled.div`
  text-align: center;
  color: #7f8c8d;
  margin-bottom: 20px;
`;

const SidebarMenu = styled.div`
  margin-top: 20px;
`;

const MenuItem = styled.div`
  padding: 12px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: #f8f9fa;
  }
  
  ${props => props.active && `
    background-color: #e8f4fc;
    color: #3498db;
    font-weight: 500;
  `}
`;

const ProfileContent = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
`;

const SectionTitle = styled.h2`
  color: #2c3e50;
  margin: 0 0 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
`;

const FormGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
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

const Select = styled.select`
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

const SaveButton = styled.button`
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 30px;
  cursor: pointer;
  font-weight: 500;
  font-size: 16px;
  
  &:hover {
    background: #2980b9;
  }
`;

const BusinessInfo = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
`;

const InfoCard = styled.div`
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
`;

const InfoIcon = styled.div`
  font-size: 24px;
  color: #3498db;
  background-color: #e8f4fc;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const InfoContent = styled.div`
  flex: 1;
`;

const InfoLabel = styled.div`
  font-size: 12px;
  color: #7f8c8d;
  text-transform: uppercase;
  margin-bottom: 3px;
`;

const InfoValue = styled.div`
  font-weight: 500;
  color: #2c3e50;
`;

function ProfilePage() {
  const [activeTab, setActiveTab] = useState('profile');
  const [profileData, setProfileData] = useState({
    fullName: "Rajesh Kumar",
    email: "rajesh@abcmanufacturing.com",
    phone: "+91-9876543210",
    businessName: "ABC Manufacturing Pvt. Ltd.",
    industry: "manufacturing",
    subcategory: "electronics",
    businessSize: "medium",
    location: "Mumbai, Maharashtra",
    legalStructure: "pvt_ltd",
    employeeCount: 150,
    annualRevenue: 50000000
  });
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleSave = () => {
    // In a real app, this would save to the backend
    alert('Profile saved successfully!');
  };
  
  return (
    <PageContainer>
      <PageTitle>Business Profile</PageTitle>
      
      <ProfileGrid>
        <ProfileSidebar>
          <Avatar>
            <FaUser />
          </Avatar>
          <UserName>{profileData.fullName}</UserName>
          <UserEmail>{profileData.email}</UserEmail>
          
          <SidebarMenu>
            <MenuItem active={activeTab === 'profile'} onClick={() => setActiveTab('profile')}>
              <FaUser /> Profile Information
            </MenuItem>
            <MenuItem active={activeTab === 'business'} onClick={() => setActiveTab('business')}>
              <FaBuilding /> Business Details
            </MenuItem>
          </SidebarMenu>
        </ProfileSidebar>
        
        <ProfileContent>
          <SectionTitle>
            {activeTab === 'profile' ? 'Profile Information' : 'Business Details'}
          </SectionTitle>
          
          {activeTab === 'profile' ? (
            <>
              <FormGrid>
                <FormGroup>
                  <Label>Full Name</Label>
                  <Input
                    type="text"
                    name="fullName"
                    value={profileData.fullName}
                    onChange={handleInputChange}
                  />
                </FormGroup>
                
                <FormGroup>
                  <Label>Email Address</Label>
                  <Input
                    type="email"
                    name="email"
                    value={profileData.email}
                    onChange={handleInputChange}
                  />
                </FormGroup>
                
                <FormGroup>
                  <Label>Phone Number</Label>
                  <Input
                    type="tel"
                    name="phone"
                    value={profileData.phone}
                    onChange={handleInputChange}
                  />
                </FormGroup>
              </FormGrid>
              
              <SaveButton onClick={handleSave}>
                Save Profile
              </SaveButton>
            </>
          ) : (
            <>
              <FormGrid>
                <FormGroup>
                  <Label>Business Name</Label>
                  <Input
                    type="text"
                    name="businessName"
                    value={profileData.businessName}
                    onChange={handleInputChange}
                  />
                </FormGroup>
                
                <FormGroup>
                  <Label>Industry</Label>
                  <Select
                    name="industry"
                    value={profileData.industry}
                    onChange={handleInputChange}
                  >
                    <option value="manufacturing">Manufacturing</option>
                    <option value="retail">Retail</option>
                    <option value="services">Services</option>
                    <option value="technology">Technology</option>
                    <option value="healthcare">Healthcare</option>
                  </Select>
                </FormGroup>
                
                <FormGroup>
                  <Label>Business Size</Label>
                  <Select
                    name="businessSize"
                    value={profileData.businessSize}
                    onChange={handleInputChange}
                  >
                    <option value="small">Small</option>
                    <option value="medium">Medium</option>
                    <option value="large">Large</option>
                  </Select>
                </FormGroup>
                
                <FormGroup>
                  <Label>Legal Structure</Label>
                  <Select
                    name="legalStructure"
                    value={profileData.legalStructure}
                    onChange={handleInputChange}
                  >
                    <option value="proprietorship">Proprietorship</option>
                    <option value="partnership">Partnership</option>
                    <option value="llp">LLP</option>
                    <option value="pvt_ltd">Private Limited</option>
                    <option value="ltd">Public Limited</option>
                  </Select>
                </FormGroup>
                
                <FormGroup>
                  <Label>Employee Count</Label>
                  <Input
                    type="number"
                    name="employeeCount"
                    value={profileData.employeeCount}
                    onChange={handleInputChange}
                  />
                </FormGroup>
                
                <FormGroup>
                  <Label>Annual Revenue (₹)</Label>
                  <Input
                    type="number"
                    name="annualRevenue"
                    value={profileData.annualRevenue}
                    onChange={handleInputChange}
                  />
                </FormGroup>
              </FormGrid>
              
              <BusinessInfo>
                <InfoCard>
                  <InfoIcon>
                    <FaMapMarkerAlt />
                  </InfoIcon>
                  <InfoContent>
                    <InfoLabel>Location</InfoLabel>
                    <InfoValue>{profileData.location}</InfoValue>
                  </InfoContent>
                </InfoCard>
                
                <InfoCard>
                  <InfoIcon>
                    <FaUsers />
                  </InfoIcon>
                  <InfoContent>
                    <InfoLabel>Employees</InfoLabel>
                    <InfoValue>{profileData.employeeCount}</InfoValue>
                  </InfoContent>
                </InfoCard>
                
                <InfoCard>
                  <InfoIcon>
                    <FaFileInvoice />
                  </InfoIcon>
                  <InfoContent>
                    <InfoLabel>Annual Revenue</InfoLabel>
                    <InfoValue>₹{profileData.annualRevenue.toLocaleString()}</InfoValue>
                  </InfoContent>
                </InfoCard>
              </BusinessInfo>
              
              <SaveButton onClick={handleSave}>
                Save Business Details
              </SaveButton>
            </>
          )}
        </ProfileContent>
      </ProfileGrid>
    </PageContainer>
  );
}

export default ProfilePage;