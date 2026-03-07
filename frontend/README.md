# TrialMatch AI - Frontend

React-based web application for matching patients with clinical trials.

## Tech Stack

- **React 18** with TypeScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **React Query** - Data fetching and caching
- **Zustand** - State management
- **Axios** - HTTP client

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── DocumentUpload/
│   ├── TrialCard/
│   ├── MatchScore/
│   └── LanguageSelector/
├── pages/              # Page components
│   ├── Home/
│   ├── Upload/
│   ├── Results/
│   └── TrialDetail/
├── services/           # API services
│   └── api.ts
├── stores/             # Zustand stores
│   └── authStore.ts
├── utils/              # Utility functions
│   └── i18n.ts
├── App.tsx             # Main app component
└── main.tsx            # Entry point
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

### Linting

Run ESLint:
```bash
npm run lint
```

## Features

### Phase 1 (Current)
- ✅ Project setup with Vite and TypeScript
- ✅ Tailwind CSS configuration
- ✅ React Router setup
- ✅ React Query configuration
- ✅ Basic page structure
- ✅ API client with interceptors

### Phase 2 (Upcoming)
- Authentication pages (Login, Register)
- Protected routes
- User profile management

### Phase 3 (Upcoming)
- Document upload with drag-and-drop
- Document processing status
- Medical profile display

### Phase 4 (Upcoming)
- Trial search and filtering
- Trial matching results
- Trial detail view

### Phase 5 (Upcoming)
- Multilingual support (5 languages)
- Favorites management
- User dashboard

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000/v1` |

## Contributing

1. Follow the existing code structure
2. Use TypeScript for type safety
3. Follow Tailwind CSS conventions
4. Write meaningful component names
5. Keep components small and focused

## License

MIT
