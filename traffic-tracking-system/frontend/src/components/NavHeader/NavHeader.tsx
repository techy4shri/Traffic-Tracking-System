import React from 'react'

const NavHeader: React.FC = () => {
  return (
    <header className="nav-header">
      <div className="nav-inner">
        <div className="nav-brand">Traffic Tracking</div>
        <nav className="nav-links">
          <a
            href="https://github.com/techy4shri/Traffic-Tracking-System#readme"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link"
          >
            About
          </a>

          <a
            href="https://github.com/sponsors/techy4shri"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link sponsor-link"
          >
            Sponsor me
          </a>

          <a
            href="https://github.com/techy4shri/Traffic-Tracking-System/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link"
          >
            Raise an issue
          </a>
        </nav>
      </div>
    </header>
  )
}

export default NavHeader
