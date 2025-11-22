import React from 'react'
import { Info, Heart, Bug } from 'lucide-react'

const NavHeader: React.FC = () => {
  return (
    <header className="nav-header" role="banner">
      <div className="nav-inner">
        <div className="nav-brand">Traffic Tracking</div>
        <nav className="nav-links" role="navigation" aria-label="Main Navigation">
          <a
            href="https://github.com/techy4shri/Traffic-Tracking-System#readme"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link"
          >
            <Info className="nav-icon" />
            <span>About</span>
          </a>

          <a
            href="https://github.com/sponsors/techy4shri"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link sponsor-link"
          >
            <Heart className="nav-icon" />
            <span>Sponsor me</span>
          </a>

          <a
            href="https://github.com/techy4shri/Traffic-Tracking-System/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link"
          >
            <Bug className="nav-icon" />
            <span>Raise an issue</span>
          </a>
        </nav>
      </div>
    </header>
  )
}

export default NavHeader
