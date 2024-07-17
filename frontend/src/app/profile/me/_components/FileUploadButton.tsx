import React, { useRef } from 'react';
import { Button } from '@chakra-ui/react';

import toast, { Toaster } from 'react-hot-toast';

const FileUploadButton = () => {
  const fileInputRef = useRef(null);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    const notify = () => toast.success('Icon image uploaded successfully');
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
        const res = await fetch(`${endpointUrl}/profile/icon`, {
          method: 'POST',
          body: formData,
          credentials: 'include' // クッキーを送信する場合に必要
        });

        if (!res.ok) {
          const data = await res.json();
        } else {
          const data = await res.json();
          notify();
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  return (
    <>
      <Button bgColor="green.200" onClick={handleButtonClick}>
        Add Icon Image
      </Button>
      <input
        type="file"
        ref={fileInputRef}
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      <Toaster />
    </>
  );
};

export default FileUploadButton;
