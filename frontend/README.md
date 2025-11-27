# React Frontend for RAG Chat

Modern React-based chat interface for the RAG-powered payment support assistant.

## 🎨 Features

- **Modern UI**: Clean, responsive design with gradient backgrounds
- **Real-time Chat**: Instant messaging with typing indicators
- **Smart Routing Display**: Shows how queries are classified and routed
- **Example Queries**: Pre-built questions in sidebar
- **Response Metadata**: Expandable details showing AI decision-making
- **Connection Status**: Real-time API connectivity monitoring
- **Mobile Responsive**: Works on all screen sizes

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- API server running on http://localhost:8000

### Installation & Launch
```bash
# Install dependencies
npm install

# Start development server
npm start

# Or use the launcher script
python run_frontend.py
```

The app will open at http://localhost:3000

## 🏗️ Architecture

### Component Structure
```
src/
├── App.js                 # Main application component
├── components/
│   └── ChatMessage.js     # Individual message component
├── services/
│   └── chatService.js     # API communication layer
└── styles/
    ├── App.css           # Component styles
    └── index.css         # Global styles
```

### Key Components

#### App.js
- Main application logic
- State management for messages and UI
- Connection status monitoring
- Example query handling

#### ChatMessage.js
- Individual message rendering
- Metadata display (expandable)
- User vs assistant styling
- Timestamp formatting

#### chatService.js
- HTTP client for API communication
- Request/response handling
- Error management
- Timeout configuration

## 🎯 User Interface

### Chat Interface
- **Message Threading**: Clear visual distinction between user and assistant
- **Typing Animation**: Shows when AI is processing
- **Scroll Behavior**: Auto-scrolls to latest messages
- **Input Validation**: Prevents empty messages

### Sidebar Features
- **Example Queries**: Click to try pre-built questions
- **How It Works**: Information about the RAG system
- **Connection Status**: Real-time service monitoring
- **Reset Button**: Clear conversation history

### Response Details
- **Query Classification**: Shows routing decision (RAG vs Direct)
- **Confidence Score**: Classification confidence percentage
- **Retrieval Count**: Number of documents retrieved
- **Response Time**: Processing duration
- **Response Type**: RAG, direct, or error

## 🔧 Configuration

### Environment Variables
```bash
# .env file (optional)
REACT_APP_API_URL=http://localhost:8000
```

### API Integration
The frontend communicates with the FastAPI backend via:
- `POST /chat` - Send messages
- `GET /status` - Check connection
- `POST /chat/reset` - Reset conversation

### Styling
- **CSS Variables**: Easy theme customization
- **Responsive Breakpoints**: Mobile-first design
- **Animations**: Smooth transitions and loading states
- **Gradient Backgrounds**: Modern visual appeal

## 🧪 Development

### Available Scripts
```bash
npm start          # Development server
npm run build      # Production build
npm test           # Run tests
npm run eject      # Eject from Create React App
```

### Development Features
- **Hot Reload**: Automatic refresh on code changes
- **Error Overlay**: Development error display
- **Source Maps**: Debugging support
- **Proxy Configuration**: API requests proxied to backend

### Code Structure
- **Functional Components**: Modern React with hooks
- **State Management**: useState and useEffect hooks
- **Error Boundaries**: Graceful error handling
- **Accessibility**: ARIA labels and keyboard navigation

## 🎨 Styling Guide

### Color Scheme
- **Primary**: Linear gradient (667eea → 764ba2)
- **Background**: Light gray (#f5f5f5)
- **Cards**: White with backdrop blur
- **Text**: Dark gray (#333) for readability

### Typography
- **Font**: System font stack for performance
- **Sizes**: Responsive scaling
- **Weights**: 400 (normal), 500 (medium), 600 (semibold)

### Layout
- **Flexbox**: Modern layout system
- **Grid**: For metadata display
- **Responsive**: Mobile-first approach
- **Spacing**: Consistent rem-based spacing

## 📱 Mobile Experience

### Responsive Design
- **Breakpoint**: 768px for mobile/desktop
- **Layout**: Stacked layout on mobile
- **Sidebar**: Collapsible on small screens
- **Touch**: Optimized for touch interactions

### Performance
- **Bundle Size**: Optimized for fast loading
- **Code Splitting**: Lazy loading where possible
- **Caching**: Browser caching for assets
- **Compression**: Gzip compression in production

## 🔍 Troubleshooting

### Common Issues

#### App won't start
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

#### API connection errors
- Check if backend is running on port 8000
- Verify CORS settings in FastAPI
- Check browser console for detailed errors

#### Styling issues
- Clear browser cache
- Check CSS import paths
- Verify CSS variables are defined

### Debug Mode
```bash
# Start with verbose logging
npm start --verbose

# Check bundle analyzer
npm run build
npx serve -s build
```

## 🚀 Production Deployment

### Build Process
```bash
# Create production build
npm run build

# Serve static files
npx serve -s build -l 3000
```

### Optimization
- **Minification**: Automatic in production build
- **Tree Shaking**: Remove unused code
- **Asset Optimization**: Image and font optimization
- **Caching**: Long-term caching headers

### Deployment Options
- **Static Hosting**: Netlify, Vercel, GitHub Pages
- **CDN**: CloudFront, CloudFlare
- **Docker**: Containerized deployment
- **Nginx**: Reverse proxy configuration

## 🔮 Future Enhancements

### Planned Features
- **Dark Mode**: Theme switching
- **Voice Input**: Speech-to-text integration
- **File Upload**: Document upload for RAG
- **Export Chat**: Download conversation history
- **Keyboard Shortcuts**: Power user features

### Technical Improvements
- **WebSocket**: Real-time streaming responses
- **State Management**: Redux for complex state
- **Testing**: Comprehensive test suite
- **PWA**: Progressive Web App features
- **Internationalization**: Multi-language support

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console errors
3. Verify API server is running
4. Check network connectivity

Happy chatting! 🎉
