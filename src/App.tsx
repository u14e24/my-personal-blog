import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Resources from './pages/resources';
import Blog from './pages/blog';
import About from './pages/about';
import Music from './pages/music'; 

import TopNavbar from './components/navbar';
import Home from './pages/home';

function App() {
  return (
    <BrowserRouter>
      <TopNavbar />
      <Home />
      <Routes>
        <Route path="/" element={<Blog />} />
        <Route path="/blog" element={<Blog />} />
        <Route path="/about" element={<About />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="/music" element={<Music />} />
      </Routes>
    </BrowserRouter>
      
);
}

export default App;