import React from "react";
import {Heart} from "lucide-react";
import {motion} from "framer-motion";

const SponsorButton: React.FC = () => (
    <motion.a href="https://github.com/sponsors/your-username"
    target="_blank"
    rel="noopener noreferrer"
    initial={{y:0}}
    animate={{y:[0,-10,0]}}
    transition={{ repeat: Infinity, duration: 1.4, ease: "easeInOut"}}
     className="fixed right-6 bottom-1/2 z-50 flex items-center gap-2 p-3 rounded-full shadow-lg bg-pink-600 hover:bg-pink-700 text-white"
    style={{
      transform: "translateY(50%)",
      textDecoration: "none",
    }}
  >
    <Heart className="w-6 h-6" />
    <span className="font-semibold hidden sm:inline">Sponsor</span>
  </motion.a>
);

export default SponsorButton;