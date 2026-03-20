# DevScope Frontend

React 18 + TypeScript + Vite dashboard for DevScope.

## Features

- **React 18** with TypeScript (strict mode)
- **Vite** for lightning-fast builds
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **Zustand** for state management
- **Axios** for API calls
- **ESLint** and **Prettier** for code quality

## Setup

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

Server runs on `http://localhost:5173`

## Build

```bash
npm run build
```

## Linting & Format

```bash
npm run lint
npm run format
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout.tsx
│   │   ├── MetricsChart.tsx
│   │   └── AnomalyAlert.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── RepositoryDetail.tsx
│   │   └── LoginPage.tsx
│   ├── hooks/
│   │   └── useAuthStore.ts
│   ├── services/
│   │   └── api.ts
│   ├── styles/
│   │   └── index.css
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

## Docker

```bash
# Build
docker build -t devscope-frontend .

# Run
docker run -p 3000:3000 devscope-frontend
```

## License

MIT
