import { SplitView } from './components/SplitView';
import { AIAdvisor } from './components/AIAdvisor';

function App() {
  return (
    <div className="min-h-screen bg-cyber-dark text-white relative">
      <SplitView />
      <AIAdvisor />
    </div>
  );
}

export default App;
