import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './App.css'
import AppRouting from './AppRouting'

function App() {
  const queryClient = new QueryClient()

  return (
    <QueryClientProvider client={queryClient}>
        <div className="App">
            <AppRouting />
        </div>
</QueryClientProvider>
  )
}

export default App
