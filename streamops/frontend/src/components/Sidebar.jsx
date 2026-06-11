import { LayoutGrid, Cpu, Rocket, ShieldCheck, Clock, FileText, HelpCircle } from 'lucide-react';
import './Sidebar.css';

const navItems = [
  { name: 'OVERVIEW', icon: LayoutGrid, active: true },
  { name: 'NODES', icon: Cpu, active: false },
  { name: 'DEPLOYMENTS', icon: Rocket, active: false },
  { name: 'SECURITY', icon: ShieldCheck, active: false },
  { name: 'HISTORY', icon: Clock, active: false },
  { name: 'DOCUMENTATION', icon: FileText, active: false },
  { name: 'SUPPORT', icon: HelpCircle, active: false },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h1 className="logo-text">VIBESYNC</h1>
      </div>
      
      <nav className="sidebar-nav">
        <ul>
          {navItems.map((item) => (
            <li key={item.name} className={`nav-item ${item.active ? 'active' : ''}`}>
              <item.icon className="nav-icon" size={18} />
              <span className="text-label nav-text">{item.name}</span>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
