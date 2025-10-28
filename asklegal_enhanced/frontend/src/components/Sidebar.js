import React from 'react';
import styled from 'styled-components';
import { 
  FaComments, 
  FaFileAlt, 
  FaClipboardCheck, 
  FaTasks, 
  FaUser, 
  FaCog
} from 'react-icons/fa';
import { useNavigate, useLocation } from 'react-router-dom';

const SidebarContainer = styled.div`
  width: 250px;
  background-color: #34495e;
  color: white;
  height: calc(100vh - 60px);
  overflow-y: auto;
`;

const MenuItem = styled.div`
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-left: 3px solid ${props => props.active ? '#3498db' : 'transparent'};
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  svg {
    font-size: 18px;
  }
`;

const MenuTitle = styled.div`
  font-size: 14px;
  font-weight: 500;
`;

const SectionTitle = styled.div`
  padding: 15px 20px 5px;
  font-size: 12px;
  text-transform: uppercase;
  color: #bdc3c7;
  letter-spacing: 1px;
`;

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  
  const menuItems = [
    {
      title: "Chat Assistant",
      icon: <FaComments />,
      path: "/chat"
    },
    {
      title: "Document Processing",
      icon: <FaFileAlt />,
      path: "/documents"
    },
    {
      title: "Compliance Check",
      icon: <FaClipboardCheck />,
      path: "/compliance"
    },
    {
      title: "Workflows",
      icon: <FaTasks />,
      path: "/workflows"
    }
  ];
  
  const userItems = [
    {
      title: "Profile",
      icon: <FaUser />,
      path: "/profile"
    },
    {
      title: "Settings",
      icon: <FaCog />,
      path: "/profile" // Redirecting to profile since there's no dedicated settings page
    }
  ];
  
  const handleNavigation = (path) => {
    navigate(path);
  };
  
  return (
    <SidebarContainer>
      <SectionTitle>Main</SectionTitle>
      {menuItems.map((item, index) => (
        <MenuItem 
          key={index}
          active={location.pathname === item.path}
          onClick={() => handleNavigation(item.path)}
        >
          {item.icon}
          <MenuTitle>{item.title}</MenuTitle>
        </MenuItem>
      ))}
      
      <SectionTitle>User</SectionTitle>
      {userItems.map((item, index) => (
        <MenuItem 
          key={index}
          active={location.pathname === item.path}
          onClick={() => handleNavigation(item.path)}
        >
          {item.icon}
          <MenuTitle>{item.title}</MenuTitle>
        </MenuItem>
      ))}
    </SidebarContainer>
  );
}

export default Sidebar;