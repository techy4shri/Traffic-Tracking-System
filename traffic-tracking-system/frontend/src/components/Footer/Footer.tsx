import { FaGithub, FaHeart, FaEnvelope, FaFileContract } from 'react-icons/fa'

const Footer = () => {
  return (
    <footer className="site-footer">
      <div className="footer-left">
        <a
          href="https://github.com/techy4shri/Traffic-Tracking-System"
          target="_blank"
          rel="noopener noreferrer"
          className="footer-icon"
        >
          <FaGithub size={32} />
        </a>
      </div>

      <div className="footer-center">
        <p className="footer-name">Garima Shrivastava</p>
        <p className="footer-tagline">Computer Vision & Deep Learning</p>
      </div>

      <div className="footer-right">
        <a href="mailto:sushri4tech@gmail.com" className="footer-icon">
          <FaEnvelope />
        </a>
        <a href="https://github.com/techy4shri/Traffic-Tracking-System/blob/main/LICENSE" 
           target="_blank" 
           rel="noopener noreferrer"
           className="footer-icon">
          <FaFileContract />
        </a>
        <a href="https://github.com/sponsors/techy4shri" 
           target="_blank" 
           rel="noopener noreferrer"
           className="footer-icon sponsor">
          <FaHeart />
        </a>
      </div>
    </footer>
  )
}

export default Footer