import React from 'react';
import styled from 'styled-components';
import { FaBars, FaUserCircle, FaTachometerAlt, FaComments, FaFileAlt, FaGavel, FaTasks, FaCogs } from 'react-icons/fa';
import { useNavigate, useLocation } from 'react-router-dom';

const HeaderContainer = styled.header`
  background-color: #2c3e50;
  color: white;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  
  span {
    color: #3498db;
  }
`;

const Nav = styled.nav`
  display: flex;
  align-items: center;
  gap: 20px;
`;

const NavItem = styled.div`
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  ${props => props.active && `
    background-color: rgba(52, 152, 219, 0.3);
  `}
`;

const UserMenu = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
`;

const UserAvatar = styled.div`
  font-size: 24px;
`;

const UserName = styled.div`
  font-size: 14px;
`;

function Header() {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <HeaderContainer>
      <Logo onClick={() => navigate('/dashboard')}>
        <FaBars style={{ marginRight: '10px' }} />
        AskLegal <span>Enhanced</span>
      </Logo>
      
      <Nav>
        <NavItem 
          active={isActive('/dashboard') || location.pathname === '/'} 
          onClick={() => navigate('/dashboard')}
        >
          <FaTachometerAlt /> Dashboard
        </NavItem>
        <NavItem 
          active={isActive('/chat')} 
          onClick={() => navigate('/chat')}
        >
          <FaComments /> Chat
        </NavItem>
        <NavItem 
          active={isActive('/document-generation')} 
          onClick={() => navigate('/document-generation')}
        >
          <FaFileAlt /> Documents
        </NavItem>
        <NavItem 
          active={isActive('/compliance')} 
          onClick={() => navigate('/compliance')}
        >
          <FaGavel /> Compliance
        </NavItem>
        <NavItem 
          active={isActive('/workflows')} 
          onClick={() => navigate('/workflows')}
        >
          <FaTasks /> Workflows
        </NavItem>
        <NavItem 
          active={isActive('/profile')} 
          onClick={() => navigate('/profile')}
        >
          <FaCogs /> Settings
        </NavItem>
      </Nav>
      
      <UserMenu onClick={() => navigate('/profile')}>
        <UserAvatar>
          <FaUserCircle />
        </UserAvatar>
        <UserName>MSME User</UserName>
      </UserMenu>
    </HeaderContainer>
  );
}

export default Header;