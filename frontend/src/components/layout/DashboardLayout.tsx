import { useState } from 'react';
import { Outlet, NavLink, Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  AlertTriangle,
  Activity,
  ChevronRight,
  Telescope,
  PanelLeftClose,
  PanelLeft,
  Menu,
  X,
  ExternalLink,
  Heart,
} from 'lucide-react';
import clsx from 'clsx';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/anomalies', label: 'Anomalies', icon: AlertTriangle },
];

export default function DashboardLayout() {
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const sidebarContent = (
    <>
      {/* Logo */}
      <Link
        to="/"
        onClick={() => setMobileOpen(false)}
        className="flex items-center gap-3 px-5 py-5 border-b border-white/[0.06] hover:bg-white/[0.02] transition-colors"
      >
        <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-brand-gradient shadow-glow flex-shrink-0">
          <Telescope className="w-5 h-5 text-white" />
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <h1 className="text-base font-bold text-white tracking-tight">DevScope</h1>
          </div>
        )}
      </Link>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {!collapsed && (
          <p className="px-3 mb-2 text-[11px] font-semibold text-gray-500 uppercase tracking-wider">
            Overview
          </p>
        )}
        {navItems.map(({ to, label, icon: Icon }) => {
          const isActive = location.pathname === to;
          return (
            <NavLink
              key={to}
              to={to}
              onClick={() => setMobileOpen(false)}
              title={collapsed ? label : undefined}
              className={clsx(
                'group flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                collapsed && 'justify-center',
                isActive
                  ? 'bg-brand-600/15 text-brand-400 shadow-sm'
                  : 'text-gray-400 hover:bg-white/[0.04] hover:text-gray-200'
              )}
            >
              <Icon
                className={clsx(
                  'w-[18px] h-[18px] transition-colors flex-shrink-0',
                  isActive ? 'text-brand-400' : 'text-gray-500 group-hover:text-gray-400'
                )}
              />
              {!collapsed && label}
              {!collapsed && isActive && (
                <ChevronRight className="w-3.5 h-3.5 ml-auto text-brand-400/60" />
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-white/[0.06]">
        {/* Collapse toggle — hidden on mobile overlay */}
        <button
          onClick={() => setCollapsed((c) => !c)}
          className="hidden lg:flex w-full items-center gap-2 px-4 py-3 text-gray-500 hover:text-gray-300 hover:bg-white/[0.03] transition-colors"
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? (
            <PanelLeft className="w-4 h-4 mx-auto" />
          ) : (
            <>
              <PanelLeftClose className="w-4 h-4" />
              <span className="text-xs">Collapse</span>
            </>
          )}
        </button>

        <div className={clsx('px-4 py-4 border-t border-white/[0.06]', collapsed && 'px-2')}>
          <div className={clsx('flex items-center', collapsed ? 'justify-center' : 'gap-2')}>
            <Activity className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
            {!collapsed && <span className="text-xs text-gray-500">System Online</span>}
          </div>
          {!collapsed && (
            <div className="mt-3 flex items-center justify-between">
              <div className="flex items-center gap-1 text-[10px] text-gray-600">
                <span>v0.1.0</span>
                <span className="text-gray-700">·</span>
                <span className="flex items-center gap-0.5">
                  Made with <Heart className="w-2.5 h-2.5 text-red-400/60" /> DevScope
                </span>
              </div>
              <a
                href="https://github.com/bereketlemma/DevScope"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-gray-400 transition-colors"
                title="View on GitHub"
              >
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          )}
        </div>
      </div>
    </>
  );

  return (
    <div className="flex h-screen bg-surface-950">
      {/* Mobile overlay backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar — desktop */}
      <aside
        className={clsx(
          'hidden lg:flex flex-col border-r border-white/[0.06] bg-surface-900/50 transition-all duration-300',
          collapsed ? 'w-[68px]' : 'w-64'
        )}
      >
        {sidebarContent}
      </aside>

      {/* Sidebar — mobile drawer */}
      <aside
        className={clsx(
          'fixed inset-y-0 left-0 z-50 w-64 flex flex-col border-r border-white/[0.06] bg-surface-900 transition-transform duration-300 lg:hidden',
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Close button */}
        <button
          onClick={() => setMobileOpen(false)}
          aria-label="Close menu"
          className="absolute top-4 right-3 p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/[0.06] transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
        {sidebarContent}
      </aside>

      {/* Main content */}
      <main className="flex-1 flex flex-col overflow-y-auto min-w-0">
        {/* Mobile top bar */}
        <div className="sticky top-0 z-30 flex items-center gap-3 px-4 py-3 border-b border-white/[0.06] bg-surface-950/90 backdrop-blur-md lg:hidden">
          <button
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/[0.06] transition-colors"
          >
            <Menu className="w-5 h-5" />
          </button>
          <Link to="/" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-md bg-brand-gradient flex items-center justify-center">
              <Telescope className="w-4 h-4 text-white" />
            </div>
            <span className="text-sm font-bold text-white">DevScope</span>
          </Link>
        </div>

        <div className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 sm:py-8">
          <Outlet />
        </div>

        {/* Main footer */}
        <footer className="border-t border-white/[0.06] bg-surface-900/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-2 text-[11px] text-gray-600">
              <div className="flex items-center gap-1.5">
                <Telescope className="w-3 h-3 text-brand-400/50" />
                <span>&copy; {new Date().getFullYear()} DevScope</span>
                <span className="text-gray-700">·</span>
                <span>Repository Intelligence Platform</span>
              </div>
              <div className="flex items-center gap-3">
                <a
                  href="https://github.com/bereketlemma/DevScope"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-gray-400 transition-colors flex items-center gap-1"
                >
                  <ExternalLink className="w-3 h-3" />
                  GitHub
                </a>
                <span className="text-gray-700">·</span>
                <span>v0.1.0</span>
              </div>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
