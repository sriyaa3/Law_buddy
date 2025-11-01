import React from 'react';
import styled from 'styled-components';

const ErrorContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
  text-align: center;
`;

const ErrorTitle = styled.h1`
  color: #e74c3c;
  font-size: 48px;
  margin-bottom: 20px;
`;

const ErrorMessage = styled.p`
  color: #2c3e50;
  font-size: 18px;
  margin-bottom: 30px;
  max-width: 600px;
`;

const ErrorButton = styled.button`
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background: #2980b9;
  }
`;

const ErrorDetails = styled.pre`
  background: #ecf0f1;
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
  max-width: 800px;
  overflow-x: auto;
  text-align: left;
  font-size: 12px;
  color: #2c3e50;
`;

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <ErrorContainer>
          <ErrorTitle>⚠️ Oops! Something went wrong</ErrorTitle>
          <ErrorMessage>
            We're sorry for the inconvenience. The application encountered an unexpected error.
            Please try reloading the page.
          </ErrorMessage>
          <ErrorButton onClick={this.handleReload}>
            Reload Page
          </ErrorButton>
          
          {process.env.NODE_ENV === 'development' && this.state.error && (
            <ErrorDetails>
              <strong>Error Details (Development Mode):</strong>
              {this.state.error && this.state.error.toString()}
              <br />
              {this.state.errorInfo && this.state.errorInfo.componentStack}
            </ErrorDetails>
          )}
        </ErrorContainer>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;