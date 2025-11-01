# AskLegal Enhanced - Frontend

React-based frontend for the AI-powered legal assistant platform specialized for MSMEs.

## Features

- **Dashboard**: Comprehensive analytics with model performance metrics
- **Chat Assistant**: AI-powered legal chat with markdown formatting
- **Document Generation**: Create and download legal documents
- **Document Processing**: Upload and analyze legal documents
- **Compliance Check**: MSME compliance verification
- **Workflows**: Guided legal workflows

## Technology Stack

- React 18.3
- React Router 6.30
- Styled Components 6.1
- React Markdown 10.1
- Axios 1.13
- React Icons 4.12

## Getting Started

### Prerequisites

- Node.js 14 or higher
- yarn package manager

### Installation

```bash
# Install dependencies
yarn install

# Start development server
yarn start
```

The application will open at `http://localhost:3000`

### Environment Variables

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_NAME=AskLegal Enhanced
REACT_APP_VERSION=2.1.0
```

## Build for Production

```bash
yarn build
```

This creates an optimized production build in the `build` folder.

## Project Structure

```
frontend/
├── public/              # Static files
├── src/
│   ├── components/      # Reusable components
│   │   ├── Header.js
│   │   ├── Sidebar.js
│   │   └── ErrorBoundary.js
│   ├── pages/          # Page components
│   │   ├── DashboardPage.js
│   │   ├── ChatPage.js
│   │   ├── DocumentGenerationPage.js
│   │   ├── DocumentPage.js
│   │   ├── CompliancePage.js
│   │   ├── WorkflowPage.js
│   │   └── ProfilePage.js
│   ├── services/       # API services
│   │   └── api.js
│   ├── App.js         # Main application component
│   ├── App.css        # Global styles
│   └── index.js       # Entry point
└── package.json       # Dependencies
```

## Key Features

### Dashboard Analytics
- Model performance comparison (SLM vs Gemini)
- Accuracy, Precision, Recall, F1-Score metrics
- Tax calculation accuracy breakdown
- Query distribution visualization
- Industry benchmark comparisons

### Chat Assistant
- Markdown-formatted responses
- Syntax highlighting for code blocks
- Real-time message streaming
- Quick action buttons
- Suggested queries

### Document Generation
- 5 document templates (NDA, Employment Contract, Service Agreement, Loan Agreement, Legal Notice)
- Dynamic form generation
- Real document download functionality
- Progress indicators

## API Integration

The frontend communicates with the FastAPI backend through the API service layer:

- **Chat API**: Send messages and retrieve chat history
- **Document API**: Upload and process documents
- **Document Generation API**: Generate and download legal documents
- **User API**: User management
- **MSME API**: Business profiles and workflows
- **Health API**: System health checks

## Error Handling

- Global error boundary for catching React errors
- API interceptors for handling network errors
- User-friendly error messages
- Automatic retry mechanisms

## Performance

- Code splitting with React.lazy
- Optimized bundle size
- Efficient re-rendering with React.memo
- Debounced API calls

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

See the main project README for contribution guidelines.

## License

See the main project LICENSE file.