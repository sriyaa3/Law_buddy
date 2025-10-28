import React from 'react';
import styled from 'styled-components';
import { FaBars, FaUserCircle } from 'react-icons/fa';

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
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
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
  return (
    <HeaderContainer>
      <Logo>
        <FaBars style={{ marginRight: '10px', cursor: 'pointer' }} />
        AskLegal <span>Enhanced</span>
      </Logo>
      
      <Nav>
        <NavItem>Dashboard</NavItem>
        <NavItem>Help</NavItem>
        <NavItem>Settings</NavItem>
      </Nav>
      
      <UserMenu>
        <UserAvatar>
          <FaUserCircle />
        </UserAvatar>
        <UserName>MSME User</UserName>
      </UserMenu>
    </HeaderContainer>
  );
}

export default Header;