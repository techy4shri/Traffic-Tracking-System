
const Background = () => {

  return (
    <div className="background-container">
      <video
        autoPlay
        muted
        loop
        playsInline
        className="background-video"
      >
        <source src="/src/assets/281611.mp4" type="video/mp4" />
      </video>
    </div>
  );
};

export default Background;