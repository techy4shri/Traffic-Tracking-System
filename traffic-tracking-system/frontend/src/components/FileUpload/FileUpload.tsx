import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FaCloudUploadAlt } from 'react-icons/fa';

interface FileUploadProps {
  onProcessed: (result: any) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onProcessed }) => {
  const [uploading, setUploading] = useState(false);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    setUploading(true);
    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/api/process', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      const result = await response.json();
      onProcessed(result);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to process the file. Please try again.');
    } finally {
      setUploading(false);
    }
  }, [onProcessed]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png'],
      'video/*': ['.mp4', '.avi', '.mov']
    },
    multiple: false
  });

  return (
    <div {...getRootProps()} className="upload-container">
      <input {...getInputProps()} />
      <FaCloudUploadAlt className="upload-icon" />
      {uploading ? (
        <p>Processing...</p>
      ) : (
        <p>{isDragActive 
          ? "Drop the file here..." 
          : "Drag & drop a file or click to select"}
        </p>
      )}
    </div>
  );
};

export default FileUpload;