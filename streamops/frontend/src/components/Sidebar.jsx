import { LayoutGrid, Cpu, Rocket, ShieldCheck, Clock, FileText, HelpCircle } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const navItems = [
  { name: 'OVERVIEW', path: '/', icon: LayoutGrid },
  { name: 'NODES', path: '/nodes', icon: Cpu },
  { name: 'DEPLOYMENTS', path: '/deployments', icon: Rocket },
  { name: 'SECURITY', path: '/security', icon: ShieldCheck },
  { name: 'HISTORY', path: '/history', icon: Clock },
  { name: 'DOCUMENTATION', path: '/docs', icon: FileText },
  { name: 'SUPPORT', path: '/support', icon: HelpCircle },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h1 className="logo-text">VIBESYNC</h1>
      </div>
      
      <nav className="sidebar-nav">
        <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
          {navItems.map((item) => (
            <li key={item.name}>
              <NavLink 
                to={item.path} 
                className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                style={{ textDecoration: 'none' }}
              >
                <item.icon className="nav-icon" size={18} />
                <span className="text-label nav-text">{item.name}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
